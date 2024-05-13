# Overview

[Yomitan](https://github.com/themoeway/yomitan)
is the main program that will create the cards. You can download Yomitan as a
[Firefox extension](https://addons.mozilla.org/en-US/firefox/addon/yomitan/)
or under the
[Chrome web store](https://chromewebstore.google.com/detail/yomitan/likgccmbimhjbgkjambclfkhldnlhbnn).

This section will go over the minimal Yomitan setup to work with this card type.

**If you have never used Yomitan before, please see
[this page](https://learnjapanese.moe/yomichan/) first to get it working.**


# Preliminary Steps
*   If you have used Yomitan before, please make a
    [backup of your settings](faq.md#how-do-i-backup-yomitan-settings)
    (just in case).

*   On top of the standard dictionaries, I highly recommend installing some frequency and
    pitch accent dictionaries, as that information is used by jp-mining-note.
    Many of these dictionaries can be found within
    [TheMoeWay's drive](https://learnjapanese.link/dictionaries).
    These dictionaries are installed in the exact same way as the standard Yomitan dictionaries.

    In particular, I recommend the [**JPDB frequency list**](https://github.com/MarvNC/jpdb-freq-list).

---


# Yomitan Fields
To edit the fields that Yomitan will automatically fill out, do the following:

![type:video](assets/setupyomitan/yomitan_anki_format.mp4)

1. Navigate to Yomitan Settings.
1. Go to the `Anki` section.
1. Select `Anki card format...`.
1. Set "Model" as `JP Mining Note`, and "Deck" to whatever your Anki deck is.
1. Copy and paste the following values into the fields
   (the custom helpers won't be available in the dropdown arrow):


??? example "Click here to see the fields to copy and paste."

    {{ yomitan_fields_table() | indent(4) }}


The above fields will create, by default,
a basic **vocab card** in **bilingual format**,
with all other definitions in collapsable fields.

!!! note
    Anything field marked with `*` are fields used to determine the resulting card type,
    and **should be configured to each user's personal preferences.**

    To change the default value of any of the fields, simply fill
    the field in within the aforementioned `Anki card format...` section.
    For example, if you want the card to be a sentence card by default,
    fill the `IsSentenceCard` field with anything, e.g. `1`.

    See the [Changing Card Type](changingcardtype.md) page for more info.


The custom helpers like `{jpmn-primary-definition}` is not provided by Yomitan by default.
See the section below to make these helpers usable.

---



# Yomitan Templates
Yomitan supports user inserted template code that allows the automatic
separation of bilingual and monolingual dictionary definitions, custom stylization, etc.
This note type makes heavy use of these custom templates.

To make the new helpers usable, do the following:

![type:video](assets/setupyomitan/import_yomitan_templates.mp4)

1. Navigate to Yomitan Settings.
1. Make sure that advanced settings are turned on (bottom left corner).
1. Go to the `Anki` section
1. Select `Configure Anki card templates...`
1. If you have existing template code already, I highly recommend
   **resetting the templates** (bottom right corner, red button)
   unless you know exactly what you are doing.

After resetting the templates,
**without** removing any of the existing template code,
add the following template code as follows:

1. Copy and paste the code below to the **top** of the default Yomitan template code:

    ??? examplecode "Click here to show the template code to copy."

        ```handlebars
        {% filter indent(width=8) -%}
        {{ TOP_YOMITAN }}
        {% endfilter %}
        ```

2. Copy and paste the code below to the **bottom** of the default Yomitan template code:

    ??? examplecode "Click here to show the template code to copy."

        ```handlebars
        {% filter indent(width=8) -%}
        {{ BOTTOM_YOMITAN }}
        {% endfilter %}
        ```

---

# Make an example card!
TODO re-record with renji's texthooker, and show result card

At this point, you should be able to make cards with Yomitan!

??? example "Click here to show some example Japanese sentences."

    「や、いらっしゃい。ま、毒を食らわば皿までって言うしね。あ、違うか。乗り掛かった船？」
    { .jp-quote-text }

    「あの時逃げ出した私の罰…あの時の汚辱は今ここで、全部そそいでやるんだ…」
    { .jp-quote-text }

    「とにかく利敵行為さえしないようにすれば基本的に問題はないはずですし、決まりきったムーブだけで絶対に勝てるというわけでも無いので、その時々の状況を落ち着いて見て、柔軟に行動することが大切です」
    { .jp-quote-text }

    「浮動小数点数は、IEEE-754規格に従って表現されています。`f32`が単精度浮動小数点数、 `f64`が倍精度浮動小数点数です」
    { .jp-quote-text }

{{ img("adding a card with Yomitan", "assets/setupyomitan/add_card.gif") }}

Obviously, just Yomitan alone doesn't fill every field.
Notably, the picture and sentence audio is missing.

Outside of that, there are some final settings you can adjust within the Yomitan templates
if the card doesn't look quite right.


---


# Monolingual Cards
If you want the first definition you see (the `PrimaryDefinition` field) to be monolingual,
change the following line at the top of the templates code:

{% raw %}
```handlebars
{{~set "opt-first-definition-type" "bilingual" ~}}
```
to
```handlebars
{{~set "opt-first-definition-type" "monolingual" ~}}
```
{% endraw %}


Additionally, a common thing that people want to do with monolingual dictionaries is to remove the first line
of the definition, because it may contain extra info that the user does not want.
See [here](definitions.md#hiding-the-first-line-of-a-definition)
to do exactly that.


!!! note

    If you are using monolingual dictionaries, on your first few cards,
    please check that your dictionaries are in the expected places.
    Extra bilingual definitions should be under `Secondary Definition`,
    and extra monolingual definitions should be under `Extra Definitions`.

    If your dictionaries are ending up in the wrong sections,
    then it is likely a problem with how the template code categorizes the dictionaries.
    See [here](definitions.md#dictionary-placement) for more info.




---




# Enjoy your new one-click cards!

If you've made it this far, then congratulations!
Most fields of the cards have been automatically filled out, just from Yomitan alone!

This concludes the minimal setup process for creating cards with Yomitan.

From here, you likely fall under one of the two categories below:


1. **I'm new to sentence mining.**

    If you're new to sentence mining, there are likely some things things
    that you would like to set up. These include:

    1. Getting the actual text to use Yomitan on.
    1. Getting the pictures and/or sentence audio from the media into the card.

    Head over to the [Setup: Text & Media](setuptextmedia.md) page to see exactly that.


1. **I already have a sentence mining workflow.**

    If you have a workflow already setup,
    you may have to do some minor tweaks to your current workflow
    to match the new field names.
    For example, the exporting sentence audio and picture fields may be different
    compared to your previous card, and have should be set to
    `SentenceAudio` and `Picture` respectively.


Finally, remember that up until now, this has been the **minimum setup** in order to use jp-mining-note.
There are likely many ways you can improve this current setup.
See the "Extra Setup" pages to the left sidebar for more information.



