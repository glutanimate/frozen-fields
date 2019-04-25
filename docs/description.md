
*Frozen Fields* allows you to conveniently **sticky and unsticky a field** right from the note editor:

![screenshot of snow-flake buttons](https://raw.githubusercontent.com/glutanimate/frozen-fields/master/screenshots/screenshot.png)

**OVERVIEW**

Anki supports **sticky fields**. A sticky field is a field whose value is not deleted when you switch to a different note. This can be very useful if you are making many notes in which a field either has the **same value** or changes very little.

Unfortunaly, marking a field as sticky is quite complex and breaks your workflow. Frozen Fields allows you to conveniently mark a field as sticky (freeze) or not sticky (unfreeze) **right from the note editor**. It’s much more convenient than the default way. 

To freeze/unfreeze a field, just **click the adjacent snowflake** or use the corresponding **hotkey** (`F9` by default). A blue snowflake means that the field is frozen and a grey snowflake means that the field is unfrozen.

**HOTKEYS**

- `F9`: toggle field between frozen and unfrozen
- `Shift + F9`: toggle status for all fields

**RELEASE LOG**

- 2019-04-25: **v2.0.2** – Fixed field display issues on Anki 2.1.12 (thanks to @ijgnd for the report!)
- 2019-04-02: **v2.0.1** – Fixed some issues on recent 2.1 releases (thanks to z1lc and ijgnd for the reports!)
- 2018-08-05: **v2.0.0** – Refactored code-base, transitioned to Anki 2.1, added config file
- 2018-01-20: Fixed snowflake icon being pasted into fields under some circumstances (thanks to [Dmitry](https://github.com/ankitest/)!)
- 2017-03-20: Refactored code-base, added hotkey for toggling all fields
- 2015-10-11: Added hotkeys
- 2012: **v1.0.0**? – Initial release by Tiago Barroso

**LATEST CHANGES AND NEWS**

*2019-04-25* **v2.0.2**

Please note that the field handling in Anki's editor has been subject to a lot of changes in recent releases. Because of that, Frozen Fields for Anki 2.1 will only work well on Anki 2.1.12 and up. If you are experiencing issues with the editor formatting please make sure to upgrade your Anki version before filing a bug report.

*2018-08-05* **v2.0.0**

This is the first public release of my fork of Tiago Barroso's *Frozen Fields* add-on. I would like to extend my heartfelt gratitude to all of what he has done for the Anki community over the years.

This update is meant to carry on his legacy by adding Anki 2.1 support, refactoring some parts of the codebase, and fixing a few smaller issues. All of this was made possible through the generous support of a fellow Anki user who would like to remain anonymous.

An overview of the most important changes in this release follows below:

- **New**: Anki 2.1 compatibility
- **New**: Hotkey for toggling all fields (default: `Shift+F9`)
- **New**: Configurable hotkeys
- **Changed**: Field toggles only appear when adding notes (having them available in the browser or while editing cards didn't make much sense)
- **Fixed**: Fix rare instances of snowflake icon being pasted into fields (thanks to [Dmitry Mikheev](https://github.com/ankitest/)!)

**CONFIGURATION**

The hotkeys can be customized by either using Anki 2.1's inbuilt add-on configuration screen (*Tools* → *Add-ons* → select *Frozen Fields* → click on *Config*), or by manually editing the corresponding config keys in `frozen_fields/meta.json` in Anki's add-on folder (Anki 2.0) [the config.json file contains the default values and **should not be modified**.].

**SUPPORT**

Please **do not report issues or bugs in the review section below**. I can only reply to your reviews in a limited fashion, so this is not a good way to strike up a dialog and track issues down. Instead, please report all issues you encounter either by creating a bug report on [GitHub](https://github.com/glutanimate/frozen-fields/issues), or by posting a new thread on the [Anki add-on support forums](https://anki.tenderapp.com/discussions/add-ons). Please make sure to include the name of the affected add-on in your report title when you do so.

**CREDITS AND LICENSE**

*Copyright © 2012-2015 [Tiago Barroso](https://github.com/tmbb)*
*Copyright © 2015-2019 [Aristotelis P.](https://glutanimate.com/)*

This add-on is based on [*Frozen Fields*](https://github.com/tmbb/FrozenFields) by [Tiago Barroso](https://github.com/tmbb). All credit for the original idea and implementation goes to him. The present fork and update to Anki 2.1 was made possible thanks to the generous support of a fellow Anki user who would like to remain anonymous.

Licensed under the [GNU AGPLv3](https://www.gnu.org/licenses/agpl.html), extended by a number of additional terms. For more information please see the license file accompanying this add-on.

The code for this add-on is available on [![GitHub icon](https://glutanimate.com/logos/github.svg) GitHub](https://github.com/glutanimate/frozen-fields).

**MORE RESOURCES**

Make sure to check out my socials for the latest add-on updates and news: [![Twitter bird](https://glutanimate.com/logos/twitter.svg)@Glutanimate](https://twitter.com/glutanimate)  |  [![YouTube playbutton](https://glutanimate.com/logos/youtube.svg) / Glutanimate](https://www.youtube.com/c/glutanimate)

Want to hire me to work on add-on for you? Get in touch at ![Email icon](https://glutanimate.com/logos/email.svg) <em>ankiglutanimate [αt] gmail .com</em>

**SUPPORT THIS ADD-ON**

Writing, supporting, and maintaining Anki add-ons like these takes a lot of time and effort. If *Frozen Fields* has been a valuable asset in your studies, please consider using one of the buttons below to support my efforts by **pledging your support on Patreon**, or by **buying me a coffee**. Each and every contribution is greatly appreciated and will help me maintain and improve *Frozen Fields* as time goes by!

[![](https://glutanimate.com/logos/patreon_button.svg)](https://www.patreon.com/glutanimate "Support me on Patreon 😄") &nbsp;&nbsp;&nbsp;&nbsp; [![](https://glutanimate.com/logos/kofi_button.svg)](https://ko-fi.com/X8X0L4YV "Buy me a coffee 😊")

*Pro-tip: Lots of exclusive add-ons and other goodies await on my Patreon page. Make sure to check them out!*
