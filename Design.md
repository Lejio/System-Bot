
Discord bot to help organize members of the GangBang Boy Scouts Discord server.
Also includes cool games!

Planned features:

- Be able to select a specific emoji on a post to allow them to join a specific gaming section.

# Database to keep track of user data:
1. Number of messages they send.
2. How often they participate in events.
3. Tokens and Coins. Both obtained through leveling up and playing games.



# Other features:
1. Collaboration with GangBang the First to implement chat-GPT and DALL-E
2. Pokemon Game
3. Learn Coding

# Pokemon:

I will try my best to create a pokemon game.

- Webscrape pokemondb.net like every month or so.
- Generate massive database. 
- Come up with some sort of leveling algorithm. (Interpolate the stat increase in each level: min -> 10, max -> 60, max level -> 50, increase stat by 1 each level).
- Depending on rarity, you would have to catch a certain amount of a pokemon in order to evolve it.
- Coins are obtained in defeating other pokemon.
- Some sort of cooldown for the pokemon?
- Private lobby/field?
- Player battles.

## Database Design:

Two tables:

- UserPokemon:
- Pokemon:

UserPokemon contains information regarding a captured pokemon. The UserPokemon database would contain all the captured pokemons in play. When the user querys for a pokemon, we would query all the pokemons under their username.

Pokemon database would contain all the pokemons currently in existence. Information in each pokemon would be it's capture rate, attacks, speed, etc.


## Game Design:

Stages (or "wild" areas) would be a discord text channel. Each stage would be of a specific type (normal, grass, water, etc.) just like the games. In order to "advance" to the next stage, you would have to defeat the gym leader in that stage. Some ideas right now for the stages: Each stage would have ~9 text channels, each resembling a generation of pokemon. So if you are specifically looking for a pokemon in generation 4, stay in the generation 4 wild area.

Legendary pokemons would spawn randomly with a lower chance spawning in lower stages, and higher chances in higher stages.

Legendary pokemons also correspond to the generation they are in.

The discord helper bot would post embedded messages with a option of fighting the pokemon. Spawning pokemons are still under development:
- The user passes a command to spawn a pokemon? (Problem is that the player can keep spamming).
- The bot spawns a couple and when one dies another spawns? (Slow gameplay and would be pretty hard to get the pokemon you want).

Pokemon getting damaged is another thing we have to figure out. When a pokemon loses HP, how would they get it back? Would a timer be placed on them to heal it back (like COC Barbarian King)? Make the player pay some coins to heal their pokemon? Both?

Battlefields would be its own object, containing things such as field effects created by both the pokemon and environments. The field object would contain two objects:
Red team pokemon and Blue team pokemon.

Battlefield would contain methods such as startRound, etc.

Battlefield would also contain the speed calculation as well.

### SHOP and COINS:

In order to earn coins, you would have to defeat pokemons in wild areas.

Each fight, you would receive a certain amount of coins based on the defeated pokemon's level.

Coins could then be used in the PokeMart to buy pokeballs to catch more pokemon, turned into tokens in which you could use that elsewhere on the discord server, heal your pokemon (controversial). Shops would be upgraded each stage.

**Current Exchange**: 1 TOKEN (not coin) --> $0.00002 and of course it would be against our TOS to exchange tokens for real money.

TOKENS are NOT crytocurrencies. The prices are set by what you could trade them for.

1 TOKEN --> 1 CHAT-GPT-3.5-TURBO Question





