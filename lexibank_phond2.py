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
    form_spec = FormSpec(
            replacements=[
                (" ", "_"),
                ("\u200b", ""),
                ("\u0009", ""),
                ("_\u0030ɔ", "_ɔ̃"),
                ("ɑ̃_ː", "ɑ̃ː"),
                ("ɛ̃_ː", "ɛ̃ː"),
                ("ɑ̃_ː", "ɑ̃ː"),
                ("aː_f̂", "âː_f"),
                ("eː_f̂", "êː_f"),
                ("ɔɐ_f̌", "ɔɐ̆_f"),
                ("ʏ_k̂", "ʏ" + "ʏ_k̂"[-1] + "_k"),
                ("a_l̂", "â_l"),
                ("ɔ_l̂", "ɔ" + "ɔ_l̂"[-1] + "_l"),
                ("a_m̂", "â_m"),
                ("i_m̂", "i" + "a_m̂"[-1] + "_m"),
                ("ɔ_m̌", "ɔ" + "ɔ_m̌"[-1] + "_m"),
                ("a_m̌", "a" + "ɔ_m̌"[-1] + "_m"),
                ("a_nː̌", "a" + "a_nː̌"[-1] + "ː_n"),
                ("ɪ_nː̌", "ɪ" + "a_nː̌"[-1] + "ː_n"),
                ("ə_n̂", "ə" + "ə_n̂"[-1] + "_n"),
                ("ɔ_l_n̂", "ɔ" + "ɔ_l_n̂"[-1] + "_l_n"),
                ("_p̂", "_p̂"[-1] + "_p"),
                ("_l_t̂", "_l_t̂"[-1] + "_l_t"),
                ("_n_t̂", "_l_t̂"[-1] + "_n_t"),
                ("ː_x̌", "ː_x̌"[-1] + "ː_x"),
                ("_x̂", "_x̂"[-1] + "_x"), 
                ("_x̌", "_x̌"[-1] + "_x"),
                ("_ç̂", "_ç̂"[-1] + "_ç"),
                ("ː_ç̌", "ː_ç̌"[-1] + "ː_ç"),
                ("_ç̌", "ː_ç̌"[-1] + "_ç"),
                ("e_ĵ", "e" + "e_ĵ"[-1] + "_j"),
                ("a_ň", "ǎ_n"),
                ("ɪ_ň", "ɪ̆_n"),
                ("ʊ_ň", "ʊ̆_n"),
                ("a_ň", "ǎ_n"),
                ("ˈˈ", "ˈ"),
                ("\u0303ɔ", "ɔ̃"),

                ],
            separators="~;,/", missing_data=["∅"], first_form_only=True)

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
            tokens = row["Tokens"].strip().split()
            #tokens = [t.replace("\u200b", "") for t in tokensf if t != "."]
            syllables = [{".": "+"}.get(t, t) for t in tokens]
            try:
                cv = "".join(tokens2class(tokens, "cv"))
            except:
                print(" ".join(tokens))
                cv = "?"
            if row["LID"] not in languages:
                errors.add(tuple(["language", row["LID"], row["LName"]]))
            else:
                args.writer.add_forms_from_value(
                        Language_ID=languages[row["LID"]],
                        Parameter_ID=concepts[row["Concept"]],
                        Value="_".join(tokens),
                        Sampa=row["Sampa"],
                        CV_Structure=row["CV"],
                        CV_Structure_Computed=cv,
                        Syllables=" ".join(syllables),
                        Source="phond2",
                        Sonority=row["Sonority"],
                        SoundClasses=row["Type"],
                        Filename=row["Filename"])

