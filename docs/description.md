
*Frozen Fields* allows you to conveniently **sticky and unsticky a field** right from the note editor:

![screenshot of snow-flake buttons](https://raw.githubusercontent.com/glutanimate/frozen-fields/blob/master/screenshots/screenshot.png)

**OVERVIEW**

Anki supports **sticky fields**. A sticky field is a field whose value is not deleted when you switch to a different note. This can be very useful if you are making many notes in which a field either has the **same value** or changes very little.

Unfortunaly, marking a field as sticky is quite complex and breaks your workflow. Frozen Fields allows you to conveniently mark a field as sticky (freeze) or not sticky (unfreeze) **right from the note editor**. It’s much more convenient than the default way. 

To freeze/unfreeze a field, just **click the adjacent snowflake** or use the corresponding **hotkey** (`F9` by default). A blue snowflake means that the field is frozen and a grey snowflake means that the field is unfrozen.

**HOTKEYS**

- `F9`: toggle field between frozen and unfrozen
- `Shift + F9`: toggle status for all fields

**RELEASE LOG**

- 2018-02-??: **v2.0.0** – Refactored code-base, transitioned to Anki 2.1, added config file
- 2018-01-20: Fixed snowflake icon being pasted into fields under some circumstances (thanks to [Dmitry](https://github.com/ankitest/)!)
- 2017-03-20: Refactored code-base, added hotkey for toggling all fields
- 2015-10-11: Added hotkeys
- 2012: **v1.0.0**? – Initial release by Tiago Barroso

**LATEST CHANGES AND NEWS**

*2018-02-??* **v2.0.0**

This is the first public release of my fork of Tiago Barroso's *Frozen Fields* add-on. I would like to extend my heartfelt gratitude to all of what he has done for the Anki community over the years.

This update is meant to carry on his legacy by adding Anki 2.1 support, refactoring some parts of the codebase, and fixing a few smaller issues. All of this was made possible through the generous support of a fellow Anki user who would like to remain anonymous.

An overview of the most important changes in this release follows below:

- **New**: Anki 2.1 compatibility
- **New**: Hotkey for toggling all fields (default: `Shift+F9`)
- **New**: Configurable hotkeys
- **Changed**: Field toggles only appear when adding notes (having them available in the browser or while editing cards didn't make much sense)
- **Fixed**: Fix rare instances of snowflake icon being pasted into fields (thanks to [Dmitry Mikheev](https://github.com/ankitest/)!)

**COMPATIBILITY**

Initial tests have shown this add-on to both work on Anki 2.0 and Anki 2.1. However, as the Anki 2.1 release line is still in beta, I cannot provide any kind of official support for this platform. **Please do not report issues with Anki 2.1 in the review section below**. Instead, please report all issues you encounter on [GitHub](https://github.com/glutanimate/frozen-fields/issues).

**CONFIGURATION**

The hotkeys can be customized by either using Anki 2.1's inbuilt add-on configuration screen (*Tools* → *Add-ons* → select *Frozen Fields* → click on *Config*), or by manually editing the corresponding config keys in `frozen_fields/meta.json` in Anki's add-on folder (Anki 2.0) [the config.json file contains the default values and **should not be modified**.].

**SUPPORT**

Please **do not report issues or bugs in the review section below**. I can't reply to your reviews, so there is no way for me to help you. Instead, please report all issues you encounter either by creating a bug report on [GitHub](https://github.com/glutanimate/frozen-fields/issues), or by posting a new thread on the [Anki add-on support forums](https://anki.tenderapp.com/discussions/add-ons). Please make sure to include the name of the affected add-on in your report title when you do so.

**CREDITS AND LICENSE**

*Copyright © 2012-2015 [Tiago Barroso](https://github.com/tmbb)*
*Copyright © 2015-2018 [Aristotelis P.](https://glutanimate.com/)*

This add-on is based on [*Frozen Fields*](https://github.com/tmbb/FrozenFields) by [Tiago Barroso](https://github.com/tmbb). All credit for the original idea and implementation goes to him.

The present fork and update to Anki 2.1 was made possible through the generous support of a fellow Anki user who would like to remain anonymous.

Licensed under the [GNU AGPLv3](https://www.gnu.org/licenses/agpl.html). The code for this add-on is available on [![GitHub icon](https://glutanimate.com/logos/github.svg) GitHub](https://github.com/glutanimate/frozen-fields).

**MORE RESOURCES**

A lot of my add-ons were commissioned by other Anki users. If you enjoy my work and would like to hire my services to work on an add-on or new feature, please feel free to reach out to me at:  ![Email icon](https://glutanimate.com/logos/email.svg) <em>ankiglutanimate [αt] gmail . com</em>

Want to stay up-to-date with my latest add-on releases and updates? Feel free to follow me on Twitter: [![Twitter bird](https://glutanimate.com/logos/twitter.svg)@Glutanimate](https://twitter.com/glutanimate)

New to Anki? Make sure to check out my YouTube channel where I post weekly tutorials on Anki add-ons and related topics: [![YouTube playbutton](https://glutanimate.com/logos/youtube.svg) / Glutanimate](https://www.youtube.com/c/glutanimate)
