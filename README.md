<p align="center"><img src="screenshots/screenshot.png"></p>

<h2 align="center">Frozen Fields for Anki</h2>

<p align="center">
<a title="Latest (pre-)release" href="https://github.com/glutanimate/frozen-fields/releases"><img src ="https://img.shields.io/github/release-pre/glutanimate/frozen-fields.svg?colorB=brightgreen"></a>
<a title="License: GNU AGPLv3" href="https://github.com/glutanimate/frozen-fields/blob/master/LICENSE"><img  src="https://img.shields.io/badge/license-GNU AGPLv3-green.svg"></a>
<a title="Rate on AnkiWeb" href="https://ankiweb.net/shared/info/516643804"><img src="https://img.shields.io/badge/ankiweb-rate-%231c93e3.svg?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAABYgAAAWIBXyfQUwAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAAJuSURBVEiJ7ZVNSBRxGMbfd3R31R11t6y2pTW1SBFCijAIAiH6INou1qVuHsSgqEOXoGMHD0LRxyFKoojCoA5qURARHqLv6ENXst3NtTZ1XWac/XTn4+lmu7W7U9qtntMw7zO/5334zzBE/7SCEhzDgLWYhxcT0DeSOPluKr2lxWV90eikCy2uyunF8HJ02xc7sutmOESn/OgYiLxEgSalZiAAZURkZWYl+35bk3h1eEbzfo0ZTk+VYCcifUGbflHUx+Oz6iSAlp9nva/lrntjCW9ASTcCMF023/YckNRww/kQwnH9M4CqP2UIJnN3SNE4IKt07MGMezKh3cgKFwDUAWguBjCrVT8azViJiG754pZWt3XrhKJ+YGJbQNJEv5Th2mqLDUA7Mz/KByj4mgKojqb0Sx2DkX39H5PzPkeZQCkVNKeD7Bam952eqXpH6Xpmjpg2AGBLqPoBKYVDo1G1tuep7BgcS+YsIaeN+euLu2tkZ1npiULwXwLCMe1h79vYxstvYhUhRSv0DBERedfZtW11FUPOcr5SzJdzyCwId9qbxHjzMguK0ono+ObqqEssOWzmywlwiyWnm2ssm3r3LO8b6fRENrhsBYPu+5OiNGfsNQsodsieCUV/VntufGW+uWgVyNflCa+qLFnLzKnfapCTzDxBwHSV7YelbXU57WwoJ7uFKZ4x6Mxz2RlNG0eLNTD7DuYbnt2xdHZ/k33IYAoys9cXydjvfkotSanGQSLqNuHk17isvnL2BNH9RFK+xbVr2TMAa9K63pkBWhcEJyIKzar9A2PJ2GRcuw5gUf+OvAKwAsD2vw7+r2x9B2aaFm6Zgef7AAAAAElFTkSuQmCC"></a>
<br>
<a title="Buy me a coffee :)" href="https://ko-fi.com/X8X0L4YV"><img src="https://img.shields.io/badge/ko--fi-contribute-%23579ebd.svg"></a>
<a title="Support me on Patreon :D" href="https://www.patreon.com/bePatron?u=7522179"><img src="https://img.shields.io/badge/patreon-support-%23f96854.svg"></a>
<a title="Follow me on Twitter" href="https://twitter.com/intent/user?screen_name=glutanimate"><img src="https://img.shields.io/twitter/follow/glutanimate.svg"></a>
</p>

> Review more, type less

*Frozen Fields* is an add-on for the spaced-repetition flashcard app [Anki](https://apps.ankiweb.net/). It allows you to conveniently sticky and unsticky a field right from within the note editor, saving you precious keystrokes when processing repetitive information.


### Table of Contents <!-- omit in toc -->

<!-- MarkdownTOC -->

- [Installation](#installation)
  - [AnkiWeb](#ankiweb)
  - [Manual installation](#manual-installation)
- [Documentation](#documentation)
- [License and Credits](#license-and-credits)

<!-- /MarkdownTOC -->

### Installation

#### AnkiWeb

The easiest way to install Frozen Fields is through [AnkiWeb](https://ankiweb.net/shared/info/516643804).

#### Manual installation

Click on the entry corresponding to your Anki version:

<details>

<summary><i>Anki 2.1</i></summary>

1. Download the latest `.ankiaddon` package from the [releases tab](https://github.com/glutanimate/frozen-fields/releases)
2. From Anki's main window, head to *Tools* → *Add-ons*
3. Drag-and-drop the `.ankiaddon` package onto the add-ons list
4. Restart Anki

</details>

<details>

<summary><i>Anki 2.1 (old versions)</i></summary>

1. Go to *Tools* → *Add-ons*
2. Click on an empty area within the add-on list to the left
3. Click on *View Files* to open the add-ons folder (named `addons21`)
4. See if the `frozen_fields` folder already exists. if so:
    1. Copy the `meta.json` file within to a safe location. This will allow you to preserve your current settings.
    2. Proceed to delete the `frozen_fields` folder
5. Download and extract the latest Anki 2.1 add-on release from the [releases tab](https://github.com/glutanimate/frozen-fields/releases)
6. Should the extracted folder not be named `frozen_fields`: Rename it to `frozen_fields`
7. Move the extracted `frozen_fields` folder into your add-ons directory (`addons21`)
8. Optional: Place the `meta.json` file back in the directory if you created a copy beforehand.
9. Restart Anki

</details>

<details>

<summary><i>Anki 2.0</i></summary>

1. Go to *Tools* → *Add-ons* → *Open add-ons folder*
2. Find and delete `Frozen Fields.py` and `frozen_fields` if they already exist
3. Download and extract the latest Anki 2.0 add-on release from the [releases tab](https://github.com/glutanimate/frozen-fields/releases)
4. Move `Frozen Fields.py` and `frozen_fields` into the add-ons folder
5. Restart Anki

</details>

### Documentation

For further information on the use of this add-on please check out [the AnkiWeb add-on description](docs/description.md).

### License and Credits

*Frozen Fields* is

*Copyright © 2012-2015 [Tiago Barroso](https://github.com/tmbb)*

*Copyright © 2015-2019 [Aristotelis P.](https://glutanimate.com/)*

The present fork is based on [*Frozen Fields*](https://github.com/tmbb/FrozenFields) by [Tiago Barroso](https://github.com/tmbb). All credit for the original idea and implementation goes to him. Initial work on this fork and the port to Anki 2.1 was made possible thanks to the generous support of a fellow Anki user who would like to remain anonymous.

Frozen Fields is free and open-source software. The add-on code that runs within Anki is released under the GNU AGPLv3 license, extended by a number of additional terms. For more information please see the [license file](https://github.com/glutanimate/frozen-fields/blob/master/LICENSE) that accompanied this program.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY. Please see the license file for more details.

----

<b>
<div align="center">The development of this add-on was made possible thanks to my <a href="https://www.patreon.com/glutanimate">Patreon</a> and <a href="https://ko-fi.com/X8X0L4YV">Ko-Fi</a> supporters.</div>
<div align="center">Thank you so much for your love and support ❤️ !</div>
</b>
