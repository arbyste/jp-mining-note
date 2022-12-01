/// {% extends "jp-mining-note/base.js" %}

/// {% block js_functions %}
{{ super() }}
/// {% endblock %}





/// {% block js_run %}
{{ super() }}

// checks leech
if (TAGS_LIST.includes("leech")) {
  LOGGER.leech();
}


/// {% call IFNOT("SentenceReading") %}
/// {% call IF("Sentence") %}
if ({{ utils.opt("no-sentence-reading-warn") }}) {
  LOGGER.warn("`SentenceReading` is not filled out. Using `Sentence` field instead.");
}
/// {% endcall %}
/// {% endcall %}

/// {% call IFNOT("Sentence") %}
/// {% call IF("SentenceReading") %}
if ({{ utils.opt("filled-sentence-reading-with-empty-sentence-warn") }}) {
  LOGGER.warn("`SentenceReading` is filled out, but the `Sentence` field is not. Is this a mistake?");
}
/// {% endcall %}
/// {% endcall %}


// removes greyed out fields if they should be hidden
if ( !{{ utils.opt("greyed-out-collapsable-fields-when-empty") }}) {
  const elems = document.getElementsByClassName("glossary-details--grey");
  for (const x of elems) {
    x.style.display = "none";
  }
}


/// {% endblock %}
