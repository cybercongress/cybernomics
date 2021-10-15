<!-- rendering hacks latex https://gist.github.com/a-rodin/fef3f543412d6e1ec5b6cf55bf197d7b#gistcomment-3523272 -->
# Bostrom Network Simulation

## Usage

0. Install Python3 if you have no
1. Go to `bostrom_simulation` folder
```bash
cd bostrom
```
2. Install requirements via pip3
```bash
pip3 install -r requirements.txt
```
3. Run
```bash
jupyter notebook
```
4. The notebook server should be running at `http://127.0.0.1:8888` 

5. Open [`simulation.ipynb`](simulation.ipynb)

6. Fill `Initial state` and `Params for simulating` sections

7. On the top bar `Kernel` -> `Restart & Run All`

8. The simulation time depends on the simulation period you have set, f.e. for 7 years it approximately 1 hour

9. Look at the results and conclude.


## Goals

To optimize parameters for launching Bostrom Network.

An idea is to model the value of BOOT token through the understanding of established network effects in Ethereum.
Then we can forecast claim dynamics and address growth based on approximated network effects. Assuming some demand for 
cyberLinks based on address growth we can adjust the supply of cyberLinks accounting for computing capability and so 
that Volt (V) token price could grow. The given model also allows defining inflation parameters of BOOT to optimize 
investments into the hardware infrastructure.


## Time 

We model Bostrom Network simulation as a (discrete) sequence of events in time. We define the `timestep` variable 
(syn `t`) as integer number of time steps since the network launch. `timestep` is used in formulas and definitions 
across this specification and defined as:

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}t = \lfloor{time\_from\_launch\_in\_years \cdot timesteps\_per\_year}\rfloor"></p>

where `time_from_launch_in_years` is time from the system launch expressed in years (float data type).

For purposes of modeling we use `timestep` equal to 1 day. The simulation period is equal to 10 years (`sim_period` `10`) .

### Simulation Parameters

- `timesteps_per_year` `(365)`
- `sim_period` `(10)`

## BOOT Supply

The BOOT supply on each `timestep` defines as the BOOT supply on the previous `timestep` plus provision on the current 
timestep:

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}boot\_supply_t = boot\_supply_{t-1} %2B timestep\_provision\_boot_t"></p>

The `timestep_provision_boot` variable is described in the [BOOT minting and inflation](#boot-minting-and-inflation) subsection.

### BOOT Minting and Inflation

The minting mechanism of Bostrom Network corresponds to the minting mechanism of 
[Cosmos Network](https://docs.cosmos.network/master/modules/mint/03_begin_block.html).

The minting mechanism was designed to:

- allow for a flexible inflation rate determined by market demand targeting a particular bonded-stake ratio
- effect a balance between market liquidity and staked supply

In order to best determine the appropriate market rate for inflation rewards, a moving change rate is used. The moving 
change rate mechanism ensures that if the `boot_bonded_share` is either over or under the `boot_bonded_share_target`, 
the inflation rate will adjust to further incentivize or disincentivize being bonded, respectively. Setting 
the `boot_bonded_share_target` at less than 100% encourages the network to maintain some non-staked tokens which 
should help provide some liquidity.

It can be broken down in the following way:

- If the inflation rate is below the `boot_bonded_share_target` the inflation rate will increase until a maximum 
value - (`boot_inflation_rate_max`) is reached
- If the `boot_bonded_share_target` (`0.80` in bostrom network) is maintained, then the inflation rate will stay 
constant
- If the inflation rate is above the goal `boot_bonded_share_target` the inflation rate will decrease until a minimum - 
value (`boot_inflation_rate_min`) is reached

In this model the target annual inflation rate is recalculated each `timestep` (in network it is recalculated each 
block). The inflation is also subject to a rate change (positive or negative) depending on the distance from the 
desired ratio. The maximum possible rate change is defined to be `boot_inflation_rate_change_annual` per year, however the 
annual inflation is capped as between `boot_inflation_rate_min` and `boot_inflation_rate_max`. In case of inflation is 
higher than `boot_inflation_rate_max` param, the inflation sets as `boot_inflation_rate_max`. In case if inflation 
lower than `boot_inflation_rate_min` param the inflation sets as `boot_inflation_rate_min`.

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}boot\_bonded\_share_{t-1} = \frac{boot\_bonded\_supply_{t-1}}{boot\_supply_{t-1}}"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}boot\_inflation\_rate\_change = \frac {({1 - \frac{boot\_bonded\_share_{t-1}}{boot\_bonded\_share\_target}}) \cdot{boot\_inflation\_rate\_change\_annual}}{timesteps\_per\_year}"></p>


<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}boot\_inflation\_rate_t = boot\_inflation\_rate_{t-1} + %2B boot\_inflation\_rate\_change"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}timestep\_provision\_boot_t = \frac{boot\_supply_{t-1} \cdot boot\_inflation\_rate_{t}}{timesteps\_per\_year}"></p>


![BOOT Supply and Inflation Rate](images/boot_supply.png)

### Initial Values

- `boot_supply` `(1e15)` 
- `boot_inflation_rate` `(0.05)`

### Simulation Parameters

- `boot_inflation_rate_max`  `(0.15)`
- `boot_inflation_rate_min`  `(0.03)`
- `boot_bonded_share_target` `(0.80)`
- `boot_inflation_rate_change_annual_annual`  `(0.20)`



## Modeling Bonded BOOT Amount (H Supply)

Agents will delegate liquid BOOT to heroes, and they will mint  corresponding 
amount of Hydrogen.

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}boot\_bonded\_supply_t = boot\_bonded\_supply_{t-1} %2B \Delta boot\_bonded\_supply"></p>

where:

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}\Delta boot\_bonded\_supply = (boot\_bonded\_share\_limit - boot\_bonded\_share_{t-1}) \cdot boot\_supply_{t-1} \cdot bonding\_speed\_coeff"></p>

For modeling puproses we model agents bonding behaviour using parameters boot_bonding_share_limit (0.85) и bonding_speed_coeff (0.01), where boot_bonding_share_limit is ratio between `boot_bonded_supply` and `boot_supply` which agents tend to have. And `bonding_speed_coeff` is speed of bonding every timestep. 

![H Supply](images/h_supply.png)

### Simulation Parameters

- `boot_bonding_share` `(0.8)`
- `hydrogen_liquid_ratio` `(0.2)`
- `boot_bonding_share_limit` `(0.85)`
- `bonding_speed_coeff` `(0.01)`

## Gift Claim Dynamics (Total refactoring of this section is needed)

The addresses for gift are defined in the [research](https://github.com/Snedashkovsky/cybergift). This research [concludes](https://github.com/Snedashkovsky/cybergift#prize-to-be-the-first) 6M addresses for distribution of 70% of BOOT tokens.

The `boot_claimed_supply` function has two phases:

- before `days_for_gift_activation`
- after `days_for_gift_activation`

It's excepted that `claimed_at_activation_share` * `boot_gift_amount_init` amount of BOOTs will be reached in 
`days_for_gift_activation`. After that, (1 - `claimed_at_activation_share`) * `boot_gift_amount_init` should be claimed 
in `days_for_gift_full_claim`.

Therefore, the `boot_claimed_supply` function can be defined as linear function with condition:

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}boot\_claimed\_supply_t = boot\_claimed\_supply_{t-1} %2B \Delta boot\_claimed\_supply"></p>

if `t` < `days_for_gift_activation`:

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}\Delta boot\_claimed\_supply = \frac{claimed\_at\_activation\_share \cdot boot\_gift\_amount\_init}{days\_for\_gift\_activation}"></p>

if `t` >= `days_for_gift_activation`:

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}\Delta boot\_claimed\_supply = \frac{(1 - claimed\_at\_activation\_share) \cdot boot\_gift\_amount\_init}{days\_for\_gift\_full\_claim}"></p>

#### `boot_to_distribution_supply`

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green} boot\_to\_distribution\_supply_t = boot\_to\_distribution\_supply_{t-1} %2B \Delta boot\_claimed\_supply %2B \Delta boot\_frozen\_supply"></p>

#### `boot_frozen_supply` Definition

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green} boot\_frozen\_supply_t = boot\_frozen\_supply_{t-1} %2B \Delta boot\_frozen\_supply"></p>

Therefore, the `delta_boot_frozen_supply` function can be represented in 3 phases:

if `t` < `days_for_gift_activation`:

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green} \Delta boot\_frozen\_supply = 0"></p>

if `t` >= `days_for_gift_activation`:

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green} \Delta boot\_frozen\_supply = boot\_to\_distribution\_supply_{t-1} \cdot 0.1"></p>

Assumptions:

- agents (`agents_count_at_activation`) will claim our gift. After that the gift will be activated
- it will take `days_for_gift_activation` since genesis before the gift claiming process will be completed
- agents on the moment of gift activation will claim share of the gift (`claimed_at_activation_share`)
- claim process can be prolonged on `days_for_gift_full_claim` in case if `agents_count_at_activation` will not reach
- the target goal by `days_for_gift_activation`
- `liquid_boot_supply_share` - is share of BOOT supply that will be in circulation from the network launch

### Simulation Parameters

- `days_for_gift_activation` `(100, 150)`
- `claimed_at_activation_share` `(1, 0.5)`
- `days_for_gift_full_claim` `(0, 360)` 
- `agents_count_at_activation` `(10'000, 50'000, 100'000)`
- `liquid_boot_supply_share` `(0.25)`

## Understanding Network Effects

### Agents Growth

To model agents' growth dynamics of the Bostrom network, we did a regression analysis on ETH active agent dynamics 
([excel spreadsheet online](https://needfordata-my.sharepoint.com/:x:/g/personal/max_needfordata_ru/EZWCgmE-VOBEsGJTg8lslpYBP2LQoBFdMC9LgXleJ3Dj_Q?e=PwmaIh)).
We calculated [ethereum active agents](eth_active_agents.ipynb) as addresses with a balance more than 0.01 ETH (the 
balance sufficient to complete at least 1 transaction).

![Dynamics of Ethereum Agents](images/eth_active_addresses_regression.png)

We have combined 2 trend lines and derived the following formula of agents counting by days from ETH dynamics.

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}agents\_count = 2 \cdot days^{2} %2B 100 \cdot days %2B 8700"></p>

Assuming that there are much more crypto-agents now than there was at the time of ETH launch, we adjusted the formula 
with coefficients to expect more rapid growth.

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}agents\_count = 9 \cdot days^2 %2B 100 \cdot days %2B agents\_count\_at\_activation"></p>

![Neurons Forecast](images/neurons_forecast.png)

### Capitalization Dynamics

We decided to model total `capitalization_in_eth` through `capitalization_per_agent` metric derived from ETH 
capitalization in BTC (from 100 day from start till 2160 days of network, as before 100 days ETH price in BTC had 
a lot of fluctuations).

![Ethereum Capitalization per Active Agent in BTC](images/eth_cap_per_active_address_in_btc_regression.png)

We derived such formula:

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}capitalization\_per\_agent\_eth\_network = 60\,000 \cdot agents\_count^{-0.7}"></p>

We assumed that dynamics of capitalization of BOOT token in ETH will resemble ETH token dynamics in BTC prices.
We adjusted the formula that our first day `capitalization_per_agent` will be equal to 32 ETH
(`start_capitalization_per_agent`).

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}capitalization\_per\_agent = start\_capitalization\_per\_agent \cdot agents\_count\_at\_activation^{0.7} \cdot  agents\_count^{-0.7}"></p>

![BOOT Capitalization](images/boot_capitalization.png)

### Simulation Parameters

- `agents_count_at_activation` `(100000)`
- `start_capitalization_per_agent` `(32)`

## Capitalization and Price

`capitalization_in_eth` in ETH is defined by formula:

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}capitalization\_in\_eth = agents\_count \cdot capitalization\_per\_agent"></p>

`gboot_price` Giga BOOT price in ETH is defined by formula:

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}gboot\_price = \frac{capitalization\_in\_eth}{boot\_supply}"></p>

![Validators Revenue](images/validators_revenue.png)

## Predicting V Demand

V are natural tokens. Each V enables its holder to produce 1 cyberlink daily. To simulate cyberlinks usage we 
have derived base estimate of `cyberlinks_per_day` formula from ETH data:

![ETH Data](images/eth_transactions_per_active_address_regression.png)

We derived such formula:

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}transactions\_per\_agent = 9 \cdot agents\_count^{-0.3}"></p>

And we adjusted such formula with adding a number of `extra_links` and `guaranteed_links`.

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}cyberlinks\_per\_day = 9 \cdot agents\_count^{-0.3} %2B extra\_links %2B guaranteed\_links"></p>

`extra_links` count depends on UX specifics, such as setting the name of agent, following (proportion of agents) and 
extra:

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}extra\_links ~ f( agents\_count, setting name, following, extra )"> 

Also, the founding team envisions some basic stuff to cyberlink such as naming systems and tokens. So we can rely on 
this demand also adding `guaranteed_links` count.

![cyberLinks Forecast](images/cyberlinks_forecast.png)

### Simulation Parameters

- `extra_links` `(0)`
- `guaranteed_links` `(0)`

## Adjusting A and V Supply

To model minting properties of V for the planning of GPU storage and maximization of V price. As Ampere (A) are 
resource tokens, and they do not have natural measure we decide to model A supply equal to V. 

System designed in the way that investminted 1 GH (1 Giga Hydrogen is equal to 1 GBOOT) for 1 day yields 1 V. 

`investmint_period` - is period of investminting H token for selected agent. It is chosen by agent according to his 
understanding and priorities of maximisation his benefits. 

And it is limited by system setting of `investmint_max_period`, that has dynamic formula written below. 

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}investmint\_max\_period = horizon\_period\_init \cdot 2^{\lceil{\log_2 \lceil{\frac{timestep %2B 1}{horizon\_period\_init}}\rceil}\rceil}"></p>

Where `horizon_period_init` (period in timesteps equal to 3 months) is the period before first `investmint_max_period` 
raise.

According to this formula current `investmint_max_period` will be set to [3, 6, 12 ... ] months.

- `ampere_base_halving_period`, `volt_base_halving_period` - time period to decrease mint_rate variable.

### Simulation Parameters

Parameters to define for A and V:
- `horizon_period_init` `(90)`

![A Halving Cycles](images/a_halving_cycles.png)
![V Halving Cycles](images/v_halving_cycles.png)

## A and V Minting

A are minted according to the following formula:

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}{ampere\_minted\_amount} = \lfloor{\frac{hydrogen\_supply}{ampere\_base\_investmint\_amount} \cdot \frac{investmint\_period}{ampere\_base\_investmint\_period} \cdot ampere\_mint\_rate}\rfloor"></p>

V are minted according to the following formula:

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}{volt\_minted\_amount} = \lfloor{\frac{hydrogen\_supply}{volt\_base\_investmint\_amount} \cdot \frac{investmint\_period}{volt\_base\_investmint\_period} \cdot volt\_mint\_rate}\rfloor"></p>

`ampere_volt_ratio` - the ratio between A and V tokens supply. 

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}ampere\_volt\_ratio = \frac{ampere\_minted\_amount}{volt\_minted\_amount}"></p>

![A Supply](images/a_supply.png)
![V Supply](images/v_supply.png)

### Simulation Parameters

- `ampere_base_investmint_amount`  `(100_000_000)`
- `volt_base_investmint_amount`  `(100_000_000)`
- `investmint_max_period_init` `(timesteps_per_year / 12)`  
- `ampere_base_investmint_period`  `(timesteps_per_year / 12)`
- `volt_base_investmint_period`  `(timesteps_per_year / 12)`
- `ampere_base_halving_period` `(12_000_000 * 6.4)`
- `volt_base_halving_period` `(12_000_000 * 6.4)`

## Mint Rate of A and V

Mint rate is multiple coefficient for minting A tokens

It is halving every `ampere_base_halving_period`

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}{ampere\_mint\_rate_t} = \frac{ampere\_mint\_rate\_init}{2^{\lfloor{\frac{t}{ampere\_base\_halving\_period}}\rfloor}}"></p>


Mint rate is multiple coefficient for minting V tokens

It is halving every `volt_base_halving_period`

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}{volt\_mint\_rate_t} = \frac{volt\_mint\_rate\_init}{2^{\lfloor{\frac{t}{volt\_base\_halving\_period}}\rfloor}}"></p>


### Assumptions

1. All agents lock tokens for the maximum available period defined in params for simulating
2. All agents mint maximum A and V tokens in 50/50 ratio


### Simulation Parameters
- `ampere_mint_rate_init` `(1)`
- `volt_mint_rate_init` `(1)`


## Planing GPU Memory Usage

We had stress testing on testnet to measure resource usage.

|             |        Now |      1B links |        100B links |
| :---------- | ---------: | ------------: | ----------------: |
| Cyberlinks  | 40,335,720 | 1,000,000,000 | 1,000,000,000,000 |
| CPU TIME, s |       0.10 |             2 |               248 |
| CPU RAM, gb |         48 |         1,183 |           118,257 |
| GPU RAM, gb |          2 |            46 |             4,562 |
| GPU TIME, s |         35 |           868 |            86,772 |
| TPS         |         10 |           248 |          6,146.39 |


According to stress testing measurements on testnet we derived formula of GPU memory usage:

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}gpu\_memory\_usage=40 \cdot cyberlinks\_count %2B 40 \cdot ampere\_minted\_amount" ></p>


![Transactions per seconds](images/transactions_per_second.png)
![GPU Memory and Time Usage](images/memory_and_time_usage.png)

## Bonding and Unbonding (Need to discuss. Probably deprecated)

The vesting function is defined as the amount of locking tokens in the time unit assumed by all liquid tokens must be
locked in the lock timeframe.

The unvesting function is defined as the amount of unlocking tokens in the time unit assumed by all locked tokens must
be unlocked in the unlock timeframe.


## Investments into Infrastructure

Target goal of simulation is to estimate revenue of 1 validator in ETH Equivalent, given that all validators have 
commission (`validator_commission`)  equals to 10% and that there are 92 validators (`max_validator_count`). 

`validator_revenue_gboot` is defined by formula:

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}validator\_revenue\_gboot = \frac{timestep\_provision\_boot \cdot validator\_commission \cdot gboot\_price}{ max\_validator\_count} "></p>


### Simulation parameters

- `validator_commission` `(0.1)`
- `max_validator_count` `(92)`


## Mathematical Specification

### Summary of simulation parameters

- `timesteps_per_year` `(365)`
- `boot_supply_init` `(1e15)`
- `boot_inflation_rate_max`  `(0.20)`
- `boot_inflation_rate_min`  `(0.05)`
- `boot_bonded_share_target` `(0.70)` 
- `boot_inflation_rate_change_annual_annual`  `(0.07)` 
- `boot_bonded_share_current` `(0.7)`
- `days_for_gift_activation` `(100, 150)`
- `claimed_at_activation_share` `(1, 0.5)`
- `days_for_gift_full_claim` `(0, 360)` 
- `agents_count_at_activation` `(10'000, 50'000, 100'000)`
- `liquid_boot_supply_share` `(0.25)`
- `agents_count_at_activation` `(100000)`
- `start_capitalization_per_agent` `(1)`
- `extra_links` `(0)`
- `guaranteed_links` `(0)`
- `horizon_period_init` `(90)`
- `ampere_volt_ratio` `(1)`  
- `ampere_base_investmint_amount`  `(100_000_000)`
- `volt_base_investmint_amount`  `(100_000_000)`
- `investmint_max_period_init` `(timesteps_per_year / 12)`  
- `ampere_base_investmint_period`  `(timesteps_per_year / 12)`
- `volt_base_investmint_period`  `(timesteps_per_year / 12)`
- `ampere_base_halving_period` `(12_000_000 * 6.4)`
- `volt_base_halving_period` `(12_000_000 * 6.4)`
- `ampere_mint_rate_init` `(1)`
- `volt_mint_rate_init` `(1)`
- `validator_commission` `(0.1)`
- `max_validator_count` `(92)`


### Formulas used as it is:

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}capitalization\_per\_agent = start\_capitalization\_per\_agent \cdot agents\_count\_at\_activation^{0.7} \cdot  agents\_count^{-0.7}"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}capitalization\_in\_eth = agents\_count \cdot capitalization\_per\_agent"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}gboot\_price=\frac{capitalization\_in\_eth}{boot\_supply}"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}validator\_revenue\_gboot = \frac{timestep\_provision\_boot \cdot validator\_commission \cdot gboot\_price}{ max\_validator\_count} "></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}{ampere\_mint\_rate_t} = \frac{ampere\_mint\_rate\_init}{2^{\lfloor{\frac{t}{ampere\_base\_halving\_period}}\rfloor}}"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}{volt\_mint\_rate_t} = \frac{volt\_mint\_rate\_init}{2^{\lfloor{\frac{t}{volt\_base\_halving\_period}}\rfloor}}"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}investmint\_max\_period = horizon\_period\_init \cdot 2^{\lceil{\log_2 \lceil{\frac{timestep %2B 1}{horizon\_period\_init}}\rceil}\rceil}"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}gpu\_memory\_usage=40 \cdot cyberlinks\_count %2B 40 \cdot ampere\_minted\_amount" ></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}ampere\_volt\_ratio = \frac{ampere\_minted\_amount}{volt\_minted\_amount}"></p>


### Formulas for Differential Equations:

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}t = \frac{timesteps\_per\_year}{365}"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}boot\_supply_t = boot\_supply_{t-1} %2B timestep\_provision\_boot_t"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}boot\_bonded\_share_t = \frac{boot\_bonded\_supply_{t-1}}{boot\_supply}"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}boot\_inflation\_rate\_change\_annual_t = \frac{1 - \frac{boot\_bonded\_share_{t-1}}{boot\_bonded\_share\_target}}{boot\_inflation\_rate\_change\_annual}"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}boot\_inflation\_rate\_change_t = \frac{boot\_inflation\_rate\_change\_annual_t}{timesteps\_per\_year}"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}boot\_inflation\_rate_t = boot\_inflation\_rate_{t-1} + %2B boot\_inflation\_rate\_change"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}timestep\_provision\_boot_t = \frac{boot\_supply_{t-1} \cdot boot\_inflation\_rate_{t}}{timesteps\_per\_year}"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}hydrogen\_supply = boot\_liquid\_supply \cdot boot\_bonded\_share\_current"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}agents\_count = 9 \cdot days^2 %2B 100 \cdot days %2B agents\_count\_at\_activation"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}transactions\_per\_agent = 9 \cdot agents\_count^{-0.3}"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}cyberlinks\_per\_day = 9 \cdot agents\_count^{-0.3} %2B extra\_links %2B guaranteed\_links"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}extra\_links ~ f( agents\_count, name, following, extra)">

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}claim(timestep) = 7 \cdot 10^{14} \cdot e^{-0.0648637 \cdot timestep}"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}{ampere\_minted\_amount} = \lfloor{\frac{hydrogen\_supply}{ampere\_base\_investmint\_amount} \cdot \frac{investmint\_period}{ampere\_base\_investmint\_period} \cdot ampere\_mint\_rate}\rfloor"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}{volt\_minted\_amount} = \lfloor{\frac{hydrogen\_supply}{volt\_base\_investmint\_amount} \cdot \frac{investmint\_period}{volt\_base\_investmint\_period} \cdot volt\_mint\_rate}\rfloor"></p>


### Differential Equations

- `boot_liquid_supply` - liquid network token amount
- `boot_bonded_supply` - bonded (staked) network token amount (H Supply)
- `boot_frozen_supply` - not claimed (frozen) network token amount
- `bonding_speed` - the amount of months to bond all liquid boots
- `unbonding_speed` - the amount of months to unbond all bonded boots
- `boot_inflation_rate` - inflation on timesep
- `boot_supply` - total network tokens supply
- `boot_inflation_rate_change_annual_annual` - maximum annual inflation rate change
- `timestep_provision_boot` - `timestep` token provision
- `ampere_supply` - A resource token amount
- `volt_supply` - V token amount
- `ampere_mint_rate` - mint rate for A token minting
- `volt_mint_rate` - mint rate for V token minting
- `cyberlinks_count` - number of cyberlinks
- `agents_count` - the amount of the active agents
- `capitalization_per_agent` - the value of agent in ETH
- `horizon_period_init` - the period before first `investmint_max_period` raise

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}boot\_inflation\_rate_t = boot\_inflation\_rate_{t-1} %2B {\Delta boot\_inflation\_rate}"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}boot\_liquid\_supply_t = boot\_liquid\_supply_{t-1} %2B {\Delta boot\_liquid\_supply}"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}boot\_bonded\_supply_t = boot\_bonded\_supply_{t-1} %2B {\Delta boot\_bonded\_supply}"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}boot\_frozen\_supply_t = boot\_frozen\_supply_{t-1} %2B {\Delta boot\_frozen\_supply}"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}ampere\_supply_t = ampere\_supply_{t-1} %2B {\Delta ampere\_supply}"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}volt\_supply_t = volt\_supply_{t-1} %2B {\Delta volt\_supply}"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}cyberlinks\_count_{t} = cyberlinks\_count_{t-1} %2B {\Delta cyberlinks\_count}"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}agents\_count_t = agents\_count_{t-1} %2B {\Delta agents\_count}"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}capitalization\_per\_agent_t = capitalization\_per\_agent_{t-1} %2B {\Delta capitalization\_per\_agent}"></p>


where the rate of change (<img src="https://render.githubusercontent.com/render/math?math=\color{green}\Delta">) is: 

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}\Delta boot\_inflation\_rate = \frac{\left(1 - \frac{boot\_bonded\_share_{t-1}}{boot\_bonded\_share\_target}\right)}{timesteps\_per\_year \cdot boot\_inflation\_rate\_change\_annual}"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}{\Delta boot\_frozen\_supply} = 45404590000000 \cdot e^{-0.0648637 \cdot x}">need to refactor</p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}{\Delta boot\_bonded\_supply} = \frac{boot\_liquid\_supply_{t-1}}{\frac{timesteps\_per\_year}{12} \cdot bonding\_speed} - {\Delta unbonded\_boot\_amount}"></p>
 
<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}{\Delta boot\_liquid\_supply} = - {\Delta boot\_frozen\_supply} - {\Delta boot\_bonded\_supply} %2B timestep\_provision\_boot_{t-1} %2B {\Delta unbonded\_boot\_amount}"></p>
 
<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}{\Delta ampere\_supply} = \lfloor{\frac{\frac{1}{2} \cdot \Delta boot\_bonded\_supply}{ampere\_base\_investmint\_amount} \cdot \frac{investmint\_max\_period_t}{ampere\_base\_investmint\_period} \cdot ampere\_mint\_rate_{t}}\rfloor"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}{\Delta volt\_supply} = \lfloor{\frac{\frac{1}{2} \cdot \Delta boot\_bonded\_supply}{volt\_base\_investmint\_amount} \cdot \frac{investmint\_max\_period_t}{volt\_base\_investmint\_period} \cdot volt\_mint\_rate_{t}}\rfloor"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}{\Delta agents\_count} = 18 \cdot t %2B 100"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}{\Delta cyberlinks\_count} = \frac{6.3}{agents\_count^{0.3}} %2B extra\_links %2B guaranteed\_links" ></p> 

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}{\Delta capitalization\_per\_agent} = - \frac{start\_capitalization\_per\_agent \cdot agents\_count\_at\_activation^{0.7}}{agents\_count^{1.7}}"></p>

where:

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}{ampere\_mint\_rate_t} = \frac{ampere\_mint\_rate\_init}{2^{\lfloor{\frac{t}{ampere\_base\_halving\_period}}\rfloor}}"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}{volt\_mint\_rate_t} = \frac{volt\_mint\_rate\_init}{2^{\lfloor{\frac{t}{volt\_base\_halving\_period}}\rfloor}}"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}timestep\_provision\_boot_{t} = \frac{boot\_supply_{t-1} \cdot boot\_inflation\_rate_{t-1}}{timesteps\_per\_year}"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}boot\_bonded\_share_{t} = \frac{boot\_bonded\_supply_{t-1}}{boot\_supply_{t-1}}"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}{investmint\_max\_period_t = investmint\_max\_period\_init \cdot 2^{\lfloor{\frac{t}{horizon\_period\_init}}\rfloor}}"></p>  


## Conclusions

![BOOT Supply and Inflation Rate](images/boot_supply.png)
![Validators Revenue](images/validators_revenue.png)
![Demand and Supply of cyberLinks](images/demand_and_supply_of_cyberlinks.png)