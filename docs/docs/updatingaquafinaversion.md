As detailed on the [home page](index.md), JPMN was originally created by
Aquafina-Water-Bottle. When Aquafina disappeared last year, I took over management
of JPMN. Unfortunately, I can't remove Aquafina's old documentation, so a lot
of people are still installing the old version of the note. At this point, the
old version of JPMN is basically unusable due to bugs.

This page is for anyone who accidentally installed the old version of JPMN, and
provides detailed instructions for updating to the latest version of the note.

---

# Checking your JPMN version

First, let's check which version of JPMN you have installed. Open up any card,
and look in the top left hand corner. If it says `jp-mining-note: v0.12.0.0-prerelease-12`,
then it means you installed the old version of JPMN, and you need to follow the
instructions on this page.

If it says `jp-mining-note: v0.12.0.0-prerelease-13` or later, then it means
you are already using the new version of JPMN. Presumably, you followed the
instructions on this site instead of Aquafina's and there's nothing further
you need to do.

---

# Replacing old versions of Anki Add-ons

Since taking over management of JPMN, two of the Anki add-ons now have new
versions. You will need to update to the new versions of the JPMN Manager add-on
and the AJT Japanese add on.

Note that neither of these add-ons are strictly required for JPMN, they just
make life substantially easier. For more info on these add-ons see
[JPMN Manager](setup.md#installing-jp-mining-note) and [AJT Japanese](setupanki.md#ajt-japanese).


1. First, uninstall the old versions of the add ons. In Anki, go to:

    > (Main Window) →  `Tools` →  `Add-ons`.

1. Look for the following add-ons. If you find them, then you need to remove
    them with the `Delete` button:
    - `JPMN Manager with prereleases`
    - `AJT Japanese`

1. You can now install the new versions of these add-ons by clicking on `Get Add-ons...`
    and pasting the following codes:
        ```
        {{ JPMN_MGR_CODE }} 200813220
        ```
    This will install the following add-ons:
    - [`JPMN Manager with prereleases New Version`](https://ankiweb.net/shared/info/301910299)
    - [`AJT Japanese for JP Mining Note`](https://ankiweb.net/shared/info/200813220)

---

# Updating Yomichan to Yomitan
If you followed the instructions in the old docs, then it is likely that you
installed Yomichan. Yomichan has now been sunset, and has been replaced by
Yomitan.

The easiest way to make sure Yomitan is correctly set up is to carefully follow
the instructions on the [Yomitan setup page](setupyomitan.md).

Note that the [Yomitan templates](setupyomitan.md#yomitan-templates) are
slightly different to the old Yomichan templates. The easiest way to make sure
they are correct is to use the red `Reset Templates` button on the templates screen
to reset the templates back to default. Then, copy the JPMN Yomitan templates
above and below the default template code.

---

# Update JPMN

You are now ready to update JPMN itself. Start [here](updating.md) and work
your way through the updating instructions.
