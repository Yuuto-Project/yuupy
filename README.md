# YuuPy <!-- omit in toc -->
_If you are interested in joining the project as a developer, please take the time to read the whole README file and join the [development server](https://discord.gg/fPFbV8G)._

YuuPy bot (formerly Yuuto or Kyuuto) is meant to be a collaboration of the [Official Camp Buddy Fan Server](https://discord.gg/campbuddy) members, completely community-driven and open source. The bot's idea came from an increasing number of tech-oriented campers asking to see or contribute to _Hiro_ (the server's custom administrative bot).  
The following documentation contains information about the whole collaborative process, as well as guidelines for developers to get everyone started from the same base. For any questions that may arise, join the [development server](https://discord.gg/fPFbV8G).

> **Note:** to start working on the bot, do not clone _master_, clone _develop_ instead. (read: [git flow](#workflow))

> **WARNING:** reading and understanding the whole README file is required before working on any part of the project. 

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
  - [First time set up](#first-time-set-up)
  - [Docker setup](#docker-setup)
  - [Bot application](#bot-application)
  - [Development](#development)
  - [Intents](#intents)
- [Development Server](#development-server)
  - [Bots](#bots)
  - [Channels](#channels)
  - [Testing channels](#testing-channels)
- [Workflow](#workflow)
  - [Latest release - Yuuto](#latest-release---Yuuto)
  - [Master branch - BabyShark](#master-branch---babyshark)
  - [Release branch ](#release-branch)
  - [Develop branch - BeachBall](#develop-branch---beachball)
  - [Feature branches - self-hosted](#feature-branches---self-hosted)
- [Code Style](#code-style)
  - [End of Line](#end-of-line)
  - [Commenting](#commenting)
  - [Commit messages](#commit-messages)
  - [Signed or Verified commits](#Signed-or-Verified-commits)

## Project Setup

YuuPy bot is written in Python and the repository hosted on GitHub, as it's the most popular platform to host Open Source project repositories. The decision for Python came from the dev team's wish for a more robust and stable platform than Node.js, but a more starter-friendly language than Kotlin.

To get started setting up the project you will need the following things:
1. Jetbrains PyCharm (The free version supports everything we need) or Visual Studio Code/Codium
2. Python 3.9 installed and set up
3. A bit of knowledge about Git/GitHub
4. Knowledge about Python

### First time set up

You will need to make and host a test bot for yourself during development. 

1. You will need to visit [Discord's developer portal](https://discord.com/developers/applications) and create a new application.
2. Click "Add a bot" in the Bot (side) menu. 
3. When you are on the bot page, scroll down to "Privileged Gateway Intents" and enable "SERVER MEMBERS INTENT".
4. Press the save button, and you are good to go running Yuuto.
5. Set up the `.env` based on the `.env.example` file.
6. Run `pip install -r requirements.txt` to download and install the project's requirements.
7. Start the bot with the `python main.py` command.

### Docker setup

1. Install docker and docker-compose (if not installed yet)
2. Copy `docker-compose.override.example.yml` to `docker-compose.override.yml` (override is ignored by git)
3. Fill in the env vars in `docker-compose.override.yml`
4. Run `docker-compose up --build` to start the bot
5. Run `docker-compose down` to stop the bot (ctrl-c works, but that does not clean up the container)

### Bot application

The bot is developed using Python 3.8 or 3.9.
Once you have cloned the repository on your local machine, make sure to set up your environment properly, as well as adding to `.gitignore` anything in your setup that hasn't yet been configured, and shouldn't be part of the bot's code.

### Development

Yuuto bot has its own development server that you can join by clicking [here](https://discord.gg/fPFbV8G). The server is the official means of discussion and collaboration on the bot, together with GitHub's collaboration tools.

### Intents

Because Yuuto uses the `GUILD_MEMBERS` gateway intent from Discord you must enable this in your developer portal.

To enable this, you have to follow the following steps:
1. Go to https://discordapp.com/developers/applications and select the application that you want to run the code on.
2. Click on the application and select "Bot" on the left side.
3. When you are on the bot page, scroll down to "Privileged Gateway Intents" and enable "SERVER MEMBERS INTENT".
4. Press the save button, and you are good to go running Yuuto.

## Development Server

The development server is the place where the campers can interact and test the bot, as for many, it might be easier than to work with GitHub's integrated tools and branches. The server also makes use of webhooks to make integration with GitHub even simpler.

> **Note**: the development server shall remain safe for work, with NSFW content allowed only in dedicated channels. Devs might want to work in public spaces such as work/university/school, and this rule is in place in order to be considerate towards them.

### Bots

To test the code in a unified environment, multiple bots will be in the server.  
_BeachBall_ is the official development bot that runs the code in the _develop_ branch. Once a user pushes code to the _develop_ branch, the bot is automatically updated. _BabyShark_ is a bot that is only active when code is ready to be released to Yuuto. _Backend_ is an administrative bot doing under the hood work that no one should pay any mind to, such as deployment server and git integrations.

For _feature_ branches, each camper/developer is welcome and encouraged to add their own testing bot to the server and using it in conjunction with the feature-testing channels to develop it. This lightens the load on BeachBall and gives you more control of the bot, such as viewing console logs or starting it up / shutting it down.

### Channels

The development server is split into different categories, which are:

- informative: channels containing official updates and webhooks,
- general: general discussion channels,
- development: channels containing development tasks and discussions, also a great place to ask for help,
- testing: different channels that are used for testing purposes.
- .ENV: channels used for testing in channel-locked mode.

### Testing channels

Testing channels are categorized based on the project branch they should be used in conjunction with (more detail in [git flow](#workflow)).

- release-testing: will only be activated to give a final test to the bot before the code is deployed
- development-testing: general testing of the code in the _develop_ branch
- feature-testing-x: channels to test using self-hosted bots running code in feature branches

## Workflow

To keep the project smooth and running, it is important to have a rigorous development process and a standardized way of doing things.

The following sections contain information about branches, and how they should be treated. If you aren't familiar with how to work with git, please familiarise yourself with its basics, and remember to ask for help from other devs should you need to. Proper git workflow and usage are crucial for the smooth operation of the project.

### Latest release - Yuuto

The _master_ branch is the most important branch and the one that mainly contains the running code of YuuPy (Yuuto). This branch is protected, and nobody, not even the maintainers can push code directly to it. The only way code can make its way to the _master_ branch is when _release_ gets merged with it by a maintainer.

Once the _release_ branch is merged into _master_ and is deemed ready for the public, it will be released using a tag. After being tagged, the official and publically available bot's code will be updated.

During the release cycle, multiple merges to the _master_ branch may be done before a tagged release to fix last-minute issues.

### Master branch - BabyShark

The _master_ branch is a branch based on _develop_ branch. This branch contains all code that would go into Yuuto before it releases to have time to fix up some issues. All code in this branch is run by BabyShark.

Work can continue on the _develop_ branch and other branches while _release_ and _master_ is being worked on, and the auditing of _release_ might take time due to external factors. 

### Release branch 

The _release_ branch is a temporary branch that is based on the _develop_ branch. It is used to initiate a new release. This branch will be merged into _master_ once the developers and the release team approve it. No new features should be merged into this branch, only fixes, and minimal changes to existing ones. After the merging is complete, this branch will get deleted.

### Develop branch - BeachBall

The _develop_ branch is the main development branch of Yuuto and the one that BeachBall is running. It is also the branch you should clone when you first join the project, as _feature_ branches will be based on it. When code is merged to this branch, BeachBall will automatically update itself to run it. Why merged? Because much like _master_, _develop_ gets updated by merges via pull requests. Force pushes to the development branch are possible, but they should only be used to update already existing core bot files in cases of important patches.

> **Note:** BeachBall is configured to restart itself if possible, and thus permanent crashes are unlikely. However, depending on the severity of the issue, permanent crashes may still occur.

### Feature branches - self-hosted

The _feature_ branches should be the main working branches for developers, and code on the _feature_ branch a dev is currently working on should be hosted by themselves to allow for maximum flexibility. 

A new branch should be created for each new feature added and in the following format: `feature/feature name`. If the feature you want to work on already has a branch, devs should work on it together instead of creating spin-offs. 

If a spin-off must be created, the following name format should be used: `feature/featurename-var[x]`, where `x` is the incremental variation number (starting with 1).

Once you or the devs working on the branch deem the feature to be complete enough for deployment to BeachBall, the _feature_ branch merges with the _develop_ branch should be initiated via a pull request.

## Code Style

When working as a team, it is important to make working with one another's code as pleasant as possible. Therefore, consistency is required, and some practices should be followed by all devs to ensure smooth teamwork and code integrity.

### End of Line

Throughout the whole project, all files should be using the _LF_ end of line separators, which is standard for Unix and macOS systems. On Windows, the default line ending is CRLF, in which case you should configure your editor to use LF line separators for the project files.

### Commenting

Your code should be well documented and commented. It is not necessary to comment every single function, loop, variable, etc. However, if the purpose of a piece of code isn't immediately clear from the naming or trivial function, some form of documentation is expected. People of various coding backgrounds, skill levels, and programming styles may work together on this project, and poor documentation or assumptions about the understanding of others are not viable.

In addition, the maintainers will have to audit the code before it is merged to _master_, and all obscure or undocumented code will be refused, no questions asked, until properly documented.

### Logging and error messages

The project uses the built-in python logging library. If you need to print a message to the console or the log, use this library. See levels of logging below for more usage information.

Using the proper level of logging is mandatory wherever it is applicable.

#### Levels of logging

- **DEBUG**: Strictly for debugging purposes where breakpoints are not feasible.
- **INFO**: Used for general reporting, shall be kept at a minimal level.
- **WARNING** (warn): Used for reporting anomalies that don't affect features and the bot's stability.
- **ERROR**: Used to warn the console about unexpected behavior and errors that can affect features.
- **CRITICAL**: Used for critical errors that can affect the bot's stability.

### Commit messages

No specific git commit message style is set in place, and you are free to name your commits however you want. However, your commit messages should still be informative and carry the essence of the commits. Any purposeful trolling or lazy commits will not be tolerated.

### Signed or Verified commits

Signing and verifying commits are not required for working on the project. Committing without a valid signature is not considered an issue in this project. If you have questions regarding this, feel free to reach out for help on the Discord server.
