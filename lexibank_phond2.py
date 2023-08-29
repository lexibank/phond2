import pathlib
import attr
from clldutils.misc import slug
from pylexibank import Dataset as BaseDataset
from pylexibank import progressbar as pb
from pylexibank import Language, Concept, Lexeme
from pylexibank import FormSpec
from lingpy import *


@attr.s
class CustomLanguage(Language):
    Number = attr.ib(default=None)
    Identifier = attr.ib(default=None)
    Site = attr.ib(default=None)
    Area = attr.ib(default=None)
    LocalID = attr.ib(default=None)

@attr.s
class CustomConcept(Concept):
    POS = attr.ib(default=None)
    Class = attr.ib(default=None)


@attr.s
class CustomLexeme(Lexeme):
    Sampa = attr.ib(default=None)
    CV_Structure = attr.ib(default=None)
    CV_Structure_Computed = attr.ib(default=None)
    SoundClasses = attr.ib(default=None)
    Sonority = attr.ib(default=None)
    Filename = attr.ib(default=None)
    Type = attr.ib(default=None)
    Syllables = attr.ib(default=None)


class Dataset(BaseDataset):
    dir = pathlib.Path(__file__).parent
    id = "phond2"
    language_class = CustomLanguage
    concept_class = CustomConcept
    lexeme_class = CustomLexeme
    form_spec = FormSpec(separators="~;,/", missing_data=["∅"], first_form_only=True)

    def cmd_makecldf(self, args):
        # add bib
        args.writer.add_sources()
        args.log.info("added sources")

        # add concept
        concepts = {}
        for row in self.concepts:
            idx = "{0}_{1}".format(row["NUMBER"], slug(row["GERMAN"]))
            args.writer.add_concept(
                    ID=idx,
                    Name=row["GERMAN"],
                    POS=row["POS"],
                    Class=row["CLASS"]
                    )
            concepts[row["GERMAN"]] = idx
        args.log.info("added concepts")

        # add language
        languages = args.writer.add_languages(lookup_factory="LocalID")
        args.log.info("added languages")

        # read in data
        data = self.raw_dir.read_csv(
            "data.tsv", delimiter="\t", quotechar=None, dicts=True
        )

        errors = set()
        for row in data:
            tokensf = row["Tokens"].strip().split()
            tokens = [t.replace("\u200b", "") for t in tokensf if t != "."]
            syllables = [{".": "+"}.get(t, t) for t in tokensf]
            try:
                cv = "".join(tokens2class(tokens, "cv"))
            except:
                print(" ".join(tokens))
                cv = "?"
            if row["LID"] not in languages:
                errors.add(tuple(["language", row["LID"], row["LName"]]))
            else:
                args.writer.add_form_with_segments(
                        Language_ID=languages[row["LID"]],
                        Parameter_ID=concepts[row["Concept"]],
                        Value=row["Tokens"],
                        Sampa=row["Sampa"],
                        CV_Structure=row["CV"],
                        CV_Structure_Computed=cv,
                        Form=row["Tokens"],
                        Segments=tokens,
                        Syllables=" ".join(syllables),
                        Source="phond2",
                        Sonority=row["Sonority"],
                        SoundClasses=row["Type"],
                        Filename=row["Filename"])

