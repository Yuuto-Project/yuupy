# yuupy <!-- omit in toc -->

_If you are interested in joining the project as a developer, please take the time to check out Kyuuto project's [docs](https://kyuuto.io/docs/)._

Kyuuto bot (formerly Yuuto) is meant to be a collaboration of the [Official Camp Buddy Fan Server](https://discord.gg/campbuddy) members, completely community driven and open source. The bot's idea came from an increasing number of tech-oriented campers asking to see or contribute to _Super Hiro_ (the server's custom administrative bot).  
The following documentation contains information about the whole collaborative process, as well as guidelines for developers to get everyone started from the same base. For any questions that may arise, join the [development server](https://discord.gg/fPFbV8G).

> **Note:** to start working on the bot, do not clone _master_, clone _develop_ instead. (read: [git flow](#workflow))

You can clone the _develop_ branch with:

```bash
git clone -b develop --single-branch https://github.com/Yuuto-Project/yuupy.git
```

or

```bash
git clone -b develop --single-branch git@github.com:Yuuto-Project/yuupy.git
```

The first command clones over HTTPS, the second one over SSH, thus requiring you to set up a key. Either command will clone the _develop_ branch **only**.

## Contents <!-- omit in toc -->

- [Project Setup](#project-setup)
  - [Bot application](#bot-application)
  - [Development](#development)
  - [Intents](#intents)
- [Development Server](#development-server)
  - [Bots](#bots)
  - [Channels](#channels)
  - [Testing channels](#testing-channels)
- [Workflow](#workflow)
  - [Master branch - Kyuuto](#master-branch---kyuuto)
  - [Release branch - BabyShark](#release-branch---babyshark)
  - [Develop branch - BeachBall](#develop-branch---beachball)
  - [Feature branches - self-hosted](#feature-branches---self-hosted)
- [Code Style](#code-style)
  - [End of Line](#end-of-line)
  - [Commenting](#commenting)
  - [Commit messages](#commit-messages)

## Project Setup

Kyuuto bot is written in Kotlin and the repository hosted on GitHub, as it's the most popular platform to host Open Source project repositories. The decision for Kotlin came from the initial JS dev team's wish for a more robust platform than Node.js.

To get started setting up the project you will need the following things:
1. Intellij IDEA (The free version supports everything we need)
2. Java 13, added to path and JAVA_HOME env var set, adopt openjdk hotspot recommended
3. A bit of knowledge about gradle
4. Knowledge about kotlin

There are a couple of important gradle commands that you need to know as well, these commands are:
- `./gradlew run` - Runs the project
- `./gradlew lintKotlin` - Runs the linter
- `./gradlew formatKotlin` - Fixes code styling (can be done with ctrl-alt-l in intellij as well)
- `./gradlew build` - Builds the project into a jar

If you are setting up the project for the first time you will need to run `./gradlew idea`.
This command will make sure you have all the proper files for intellij to function correctly. Alternatively you can also run `./gradlew openIdea` to open your intellij installation from the command line directly.

Note: If you are a Windows user you will need to use `gradlew.bat` instead of `./gradlew`

### Bot application

The bot is developed using Kotlin, for JDK 13.
Once you have cloned the repository on your local machine, make sure to set up your environment properly, as well ad adding to `.gitignore` anything in your setup that hasn't yet been configured, and shouldn't be part of the bot's code

### Development

Yuuto bot has its own development server, you can join it by clicking [here](https://discord.gg/fPFbV8G). The server is the official means of discussion and collaboration on the bot, together with GitHub's collaboration tools.

### Intents

Because Yuuto is using the `GUILD_MEMBERS` gateway intent from discord you must enable this in your developer portal.

To enable this you have to follow the following steps:
1. Go to https://discordapp.com/developers/applications and select the application that you want to run the code on.
2. Click on the application and select "Bot" on the left side.
3. When you are on the bot page scroll down to "Privileged Gateway Intents" and enable "SERVER MEMBERS INTENT".
4. Press the save button and you are good to go to run Yuuto.

## Development Server

The development server is the place where the campers can interact and test the bot, as for many it might be easier than to work with GitHub's integrated tools and branches. The server also makes use of webhooks to make integration with GitHub even simpler.

> **Note**: the development server shall remain safe for work, with NSFW content allowed only in dedicated channels. Devs might be wanting to work in public spaces such as work / university / school, and this rule is in place in order to be considerate towards them.

### Bots

To test the code in a unified environment, multiple bots will be in the server.  
_BeachBall_ is the official development bot that runs the code in the _develop_ branch. Once a user pushes code to the _develop_ branch, the bot is automatically updated. _BabyShark_ is a bot that is only active when code is ready to be released to Yuuto. _Backend_ is an administrative bot doing under the hood work that one should pay no mind to, such as deployment server and git integrations.

For _feature_ branches, each camper / developer is welcome and encouraged to add their own testing bot to the server and using it in conjunction with the feature-testing channels to develop it. This lightens the load on BeachBall and gives you more control of the bot such as viewing console logs or starting it up / shutting it down.

### Channels

The development server is split into different categories, which are:

- informative: channels containing official updates and webhooks,
- general: general discussion channels,
- development: channels containing development tasks and discussions, also a great place to ask for help,
- testing: different channels that are used for testing purposes.

### Testing channels

Testing channels are categorised based on the project branch they should be used in conjunction with (more detail in [git flow](#workflow)).

- release-testing: will only be activated to give a final test to the bot before the code is deployed
- development-testing: general testing of the code in the _develop_ branch
- feature-testing-x: branches to test bots in feature branches
- special-channel-x: channels corresponding to specific channels in the CB server

## Workflow

To keep the project smooth and running, it is important to have a rigorous development process and a standardised way of doing things.

The following sections contain information about branches, and how they should be treated. If you aren't familiar with how to work with git, please familiarise yourself with its basics, and remember to ask for help from other devs should you need to. Proper git workflow and usage is crucial for the smooth operation of the project.

> **Note:** more in-depth documentation/help available on the [Kyuuto Docs](https://kyuuto.io/kb/yuuto-flow/).

### Master branch - Kyuuto

The _master_ branch is the most important branch and the one that contains the running code of Kyuuto (Yuuto). This branch is protected and nobody, not even the maintainers can push code to it directly. The only way code can make its way to the _master_ branch, is when _release_ gets merged with it by a maintainer.

### Release branch - BabyShark

The _release_ branch is a branch based off _develop_ branch, and any additions to it should only contain bug fixes, quality improvements and final polishes. This branch is created once enough or noticeable features on _develop_ get finalised, and it is time to deploy them to Yuuto. The code in the _release_ branch is ran by BabyShark. Once a maintainer merges _release_ with _master_, the branch gets deleted.

Work can continue on the _develop_ branch and other branches while _release_ is being worked on, and the auditing of _release_ might take time due to external factors. After the branch is deleted, work will resume as previously, and BabyShark will be toggled off.

### Develop branch - BeachBall

The _develop_ branch is the main development branch of Yuuto and the one that BeachBall is running. It is also the branch you should clone when you first join the project, as _feature_ branches will be based off it. When code is merged to this branch, BeachBall will automatically update itself to run it. Why merged? Because much like _master_, _develop_ gets updated by merges via pull requests. Force pushes to the development branch are possible, however they should be used only to update already existing core bot files in cases of important patches.

> **Note:** BeachBall is configured to restart itself if possible and thus permanent crashes are unlikely. However, depending on the severity of the issue, permanent crashes may still occur.

### Feature branches - self-hosted

The _feature_ branches should be the main working branches for developers, and code on the _feature_ branch a dev is currently working on should be hosted by themselves to allow for maximum flexibility. A new branch should be created for each new feature added and in the following format: `feature/featurename`. If the feature you want to work on already has a branch, devs should work on it together instead of creating spin-offs. If a spin-off must be crated, the following name format should be used: `feature/featurename-var[x]`, where `x` is the incremental variation number (starting with 1).

Once you or the devs working on the branch deem the feature to be complete enough for deployment to BeachBall, the _feature_ branch merge with the _develop_ branch should be initiated via a pull request.

## Code Style

When working as a team, it is important to make working with one another's code as pleasant as possible. Therefore, consistency is required, and some practices should be followed by all devs so ensure smooth teamwork and code integrity.

### End of Line

Throughout the whole project, all files should be using the _LF_ end of line separators, which is standard for Unix and macOS systems. On Windows, the default line ending is CRLF, in which case you should configure your editor to use LF line separators for the project files.

### Commenting

Your code should be well documented and commented. It is not necessary to comment every single function, loop, variable, ... however if the purpose of a piece of code isn't immediately clear from the naming or trivial function, some form of documentation is expected. People of various coding backgrounds, skill levels and programming styles may work together on this project, and poor documentation or assumptions about the understanding of others are not viable.  
In addition, the maintainers will have to audit the code before it is merged to _master_, and all obscure or undocumented code will be refused, no questions asked, until properly documented.

### Commit messages

No specific git commit message style is set in place and you are free to name your commits however you want, however your commit messages should still be informative and carry the essence of the commits. Any purposeful trolling or lazy commits will not be tolerated.