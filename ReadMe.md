[![Issues](https://img.shields.io/github/issues/jainamoswal/BotStatus?style=for-the-badge&color=green)](https://github.com/jainamoswal/BotStatus/issues)
[![Forks](https://img.shields.io/github/forks/jainamoswal/BotStatus?style=for-the-badge&color=green)](https://github.com/jainamoswal/BotStatus/fork)
[![Stars](https://img.shields.io/github/stars/jainamoswal/BotStatus?style=for-the-badge&color=green)](https://github.com/jainamoswal/BotStatus)
[![LICENSE](https://img.shields.io/github/license/jainamoswal/BotStatus?color=green&style=for-the-badge)](https://github.com/jainamoswal/BotStatus)
[![Size](https://img.shields.io/github/repo-size/jainamoswal/BotStatus?style=for-the-badge&color=green)](https://github.com/jainamoswal/BotStatus)
[![Contributors](https://img.shields.io/github/contributors/jainamoswal/BotStatus?style=for-the-badge&color=green)](https://github.com/jainamoswal/BotStatus)



## BotStatus ~ 

A simple & short repository to show your bot's status in your GitHub README.md file as well as in you channel. 

---
### How to use this ?

- **Star** this repo. ⭐
- Go to the repository where you want to display the status of the bots. 🤖
- Go to environment variables ([Settings ⇢ Secrets ⇢ New Repository Secret.](https://docs.github.com/en/actions/reference/encrypted-secrets)) 🚶
- Fill all Environment variables there. 🤭
- Copy [this](./example.yml) snippet in `./github/workflows/main.yml` in your repository. 📁
- The workflow will automatically run at interval of 3 hours. 🏃
  
_⚠️ You'll need a bots.json file and list all bots in the JSON format.
It can be raw link from `gist.github.com` or directly by the file itself like `https://github.com/<blabla>/raw/<branchname>/<filename>`. But it should point to the raw source._ 

<details>
  <summary><b>🤫&nbsp;Environment variables</b></summary>
  <br/>

| 🔒 Secret 🔒 | ✍️ Description ✍️ |
| :-: | :-: |
| API_HASH | Get it from [my.telegram.org](https://my.telegram.org) |
| APP_ID | Get it from [my.telegram.org](https://my.telegram.org) |
| CHANNEL_ID | Channel ID eg. -10010254xxxxx |
| MESSAGE_ID | Message ID of the message to edit. |
| SESSION | [![Run on Repl.it](https://replit.com/badge/github/jainamoswal/SessionString)](https://replit.com/@jainamoswal/SessionString) |
| BOTS | Raw link of JSON file of bots. [example](./example.json) |
</details>


<details>
  <summary><b>:v: &nbsp;Support me</b></summary>
  <br/>
  <p align="center">
    <a href="https://paypal.com/paypalme/JOswal105">
        <img height="40px" src="https://www.paypalobjects.com/webstatic/mktg/Logo/pp-logo-100px.png" />
    </a> &nbsp;
    <a href="https://buymeacoffee.com/jainamoswal">
        <img height="40px" src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" />
    </a> &nbsp;
    <a href="https://ko-fi.com/O5O64S9GG">
        <img height="40px" src="https://cdn.ko-fi.com/cdn/kofi3.png?v=2" />
    </a> &nbsp;
    <a href="https://upier.org/pay?vpa=jainamoswal@sbi&amount=250">
        <img height="40px" src="https://upload.wikimedia.org/wikipedia/commons/archive/e/e1/20200901100646%21UPI-Logo-vector.svg" />
    </a>
  </p>
  
</details>

<details>
  <summary><b>💻&nbsp;Credits</b></summary>
  <br/>

- [xditya](https://github.com/xditya) for inspiration from [his repo.](https://github.com/xditya/BotStatus)
- [Lonami](https://github.com/LonamiWebs) for telethon.
- [Google](https://google.com) and [Telethon docs](https://docs.telethon.dev/en/latest)  😅
</details>

<hr/>

## License 
### [BotStatus](https://github.com/jainamoswal/BotStatus) is licensed under [GNU Affero General Public License v3](https://www.gnu.org/) or later.

[![License](https://www.gnu.org/graphics/gplv3-or-later.png)](LICENSE)

`The GNU General Public License (GNU GPL or simply GPL) is a series of widely-used free software licenses that guarantee end users the freedom to run, study, share, and modify the software.[8] The licenses were originally written by Richard Stallman, founder of the Free Software Foundation (FSF), for the GNU Project, and grant the recipients of a computer program the rights of the Free Software Definition.[9] The GPL series are all copyleft licenses, which means that any derivative work must be distributed under the same or equivalent license terms. This is in distinction to permissive software licenses, of which the BSD licenses and the MIT License are widely used, less restrictive examples. GPL was the first copyleft license for general use.`
