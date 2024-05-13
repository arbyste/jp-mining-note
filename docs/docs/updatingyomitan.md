This section is dedicated to updating Yomitan settings required to use JPMN.


---


# Updating Yomitan's Anki Card Format

To update the Yomitan Format, the steps should be almost the same as the
one specified already in the [setup](setupyomitan.md#yomitan-fields).
The most important difference is that if a new field was added or a field has been renamed,
then **the field will not show up automatically in Yomitan**.


## Refreshing Yomitan Fields

??? example "Video Demo <small>(click here)</small>"
    ![type:video](assets/updating/updating_yomitan_fields.mp4)

    TODO update the video...

1. As always, create a [backup](faq.md#how-do-i-backup-yomitan-settings)
    of your Yomitan settings, just in case.
1. After installing the note update, create a temporary copy of the note by: <br>
    `Tools` <br>
    →  `Manage Note Types` <br>
    →  `Add` <br>
    →  Select `Clone: JP Mining Note` →  `Ok` <br>
    →  Name this to anything you want. The following examples will use `JP Mining Note copy`. <br>
    →  `Ok`<br>
    →  `Close`
1. If you are currently viewing Yomitan Settings, please refresh the page.
1. Head over to Anki Card Format [as before](setupyomitan.md#yomitan-fields).
1. In the top right corner, change `Model` to `JP Mining Note copy`,
    and then change it back to `JP Mining Note`.
    (If you don't see `JP Mining Note copy`, please refresh the page.)
1. Update the fields as specified.
    - It should be specified in the text you see when updating.
        However, you should also simply compare the table on the
        [setup page](setupyomitan.md#yomitan-fields) to your filled out fields.
1. Remove the temporary note: <br>
    `Tools` <br>
    →  `Manage Note Types` <br>
    →  (select `JP Mining Note copy`) <br>
    →  `Delete`

!!! info "Explanation"
    Using the temporary copy of the updated card
    means that fields that remain unchanged between the old card and new card
    will be transferred automatically in the Yomitan Format.
    If you simply choose some random model like `Basic`,
    then almost none of the fields will be preserved, as the `Basic` card
    does not have any matching fields with the `JP Mining Note` model.

---


# Updating Yomitan Templates
Like the above, you can simply follow the steps already specified in [setup](setupyomitan.md#yomitan-templates).

Again, please make a [backup](faq.md#how-do-i-backup-yomitan-settings)
of your Yomitan settings just in case,
and again, please make sure you **reset the existing templates** (unless you know what you are doing).

Note that your Yomitan template options will be reset if you follow all the steps.
I recommend temporarily saving a copy of the Yomitan templates so you can easily
reset your Yomitan template options after updating.


---
