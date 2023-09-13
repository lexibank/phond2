## Specification of form manipulation


Specification of the value-to-form processing in Lexibank datasets:

The value-to-form processing is divided into two steps, implemented as methods:
- `FormSpec.split`: Splits a string into individual form chunks.
- `FormSpec.clean`: Normalizes a form chunk.

These methods use the attributes of a `FormSpec` instance to configure their behaviour.

- `brackets`: `{'(': ')'}`
  Pairs of strings that should be recognized as brackets, specified as `dict` mapping opening string to closing string
- `separators`: `~;,/`
  Iterable of single character tokens that should be recognized as word separator
- `missing_data`: `['∅']`
  Iterable of strings that are used to mark missing data
- `strip_inside_brackets`: `True`
  Flag signaling whether to strip content in brackets (**and** strip leading and trailing whitespace)
- `replacements`: `[(' ', '_'), ('\u200b', ''), ('\t', ''), ('_0ɔ', '_ɔ̃'), ('ɑ̃_ː', 'ɑ̃ː'), ('ɛ̃_ː', 'ɛ̃ː'), ('ɑ̃_ː', 'ɑ̃ː'), ('aː_f̂', 'âː_f'), ('eː_f̂', 'êː_f'), ('ɔɐ_f̌', 'ɔɐ̆_f'), ('ʏ_k̂', 'ʏ̂_k'), ('a_l̂', 'â_l'), ('ɔ_l̂', 'ɔ̂_l'), ('a_m̂', 'â_m'), ('i_m̂', 'î_m'), ('ɔ_m̌', 'ɔ̌_m'), ('a_m̌', 'ǎ_m'), ('a_nː̌', 'ǎː_n'), ('ɪ_nː̌', 'ɪ̌ː_n'), ('ə_n̂', 'ə̂_n'), ('ɔ_l_n̂', 'ɔ̂_l_n'), ('_p̂', '̂_p'), ('_l_t̂', '̂_l_t'), ('_n_t̂', '̂_n_t'), ('ː_x̌', '̌ː_x'), ('_x̂', '̂_x'), ('_x̌', '̌_x'), ('_ç̂', '̂_ç'), ('ː_ç̌', '̌ː_ç'), ('_ç̌', '̌_ç'), ('e_ĵ', 'eĵ_j'), ('a_ň', 'ǎ_n'), ('ɪ_ň', 'ɪ̆_n'), ('ʊ_ň', 'ʊ̆_n'), ('a_ň', 'ǎ_n'), ('ˈˈ', 'ˈ'), ('̃ɔ', 'ɔ̃')]`
  List of pairs (`source`, `target`) used to replace occurrences of `source` in formswith `target` (before stripping content in brackets)
- `first_form_only`: `True`
  Flag signaling whether at most one form should be returned from `split` - effectively ignoring any spelling variants, etc.
- `normalize_whitespace`: `True`
  Flag signaling whether to normalize whitespace - stripping leading and trailing whitespace and collapsing multi-character whitespace to single spaces
- `normalize_unicode`: `None`
  UNICODE normalization form to use for input of `split` (`None`, 'NFD' or 'NFC')