/// {% extends "jp-mining-note/base.js" %}

/// {% block js_run %}
{{ super() }}

{ // auto-plays sentence audio on the front side of the audio card
  let elem = document.querySelector("#sentence-audio .soundLink, #sentence-audio .replaybutton");
  if (elem) {
    elem.click();
  }
}

/// {% endblock %}
