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

To optimize parameters for launching the Bostrom Network.

We model the value of the BOOT token through the understanding of established network effects in Ethereum.
Further, we forecast gift claim dynamics and address growth based on approximated network effects. Assuming some
demand for cyberLinks based on address growth we adjust the supply of cyberLinks accounting for computing
capability and the growth of Volt (V) token price. The given model also allows defining inflation parameters of
BOOT to optimize investments into the hardware infrastructure.


## Time

We model Bostrom Network simulation as a (discrete) sequence of events in time. We define the `timestep` variable
(syn `t`) as an integer number of time steps since the network launch. `timestep` is used in formulas and
definitions across this specification and defined as:

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}t = \lfloor{time\_from\_launch\_in\_years \cdot timesteps\_per\_year}\rfloor"></p>

where `time_from_launch_in_years` is time from the system launch expressed in years (float data type).

For purposes of modeling we use `timestep` equal to 1 day. The simulation period is equal to 10 years
(`sim_period` `10`) .

### Simulation Parameters

- `timesteps_per_year` `(365)`
- `sim_period` `(10)`

## BOOT Supply

The BOOT supply on each `timestep` defines as the BOOT supply on the previous `timestep` plus provision on the
current timestep:

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}boot\_supply_t = boot\_supply_{t-1} %2B timestep\_provision\_boot_t"></p>

The `timestep_provision_boot` variable is described in the
[BOOT minting and inflation](#boot-minting-and-inflation) subsection.

### BOOT Minting and Inflation

The minting mechanism of the Bostrom Network corresponds to the minting mechanism of the
[Cosmos Network](https://docs.cosmos.network/master/modules/mint/03_begin_block.html).

The minting mechanism was designed to:

- allow for a flexible inflation rate determined by market demand targeting a particular bonded-stake ratio
- effect a balance between market liquidity and staked supply

In order to best determine the appropriate market rate for inflation rewards, a moving change rate is used. The
moving change rate mechanism ensures that if the `boot_bonded_share` is either over or under the
`boot_bonded_share_target`, the inflation rate will adjust to further incentivize or disincentivize being bonded,
respectively. Setting the `boot_bonded_share_target` at less than 100% encourages the network to maintain some
non-staked tokens which should help provide some liquidity.

It can be broken down in the following way:

- If the inflation rate is below the `boot_bonded_share_target` the inflation rate will increase until a maximum
  value - (`boot_inflation_rate_max`) is reached
- If the `boot_bonded_share_target` (`0.80` in bostrom network) is maintained, then the inflation rate will stay
  constant
- If the inflation rate is above the goal `boot_bonded_share_target` the inflation rate will decrease until a
  minimum - value (`boot_inflation_rate_min`) is reached

In this model the target annual inflation rate is recalculated each `timestep` (in the network it is recalculated
each block). The inflation is also subject to a rate change (positive or negative) depending on the distance from
the desired ratio. The maximum possible rate change is defined to be `boot_inflation_rate_change_annual` per
year, however, the annual inflation is capped as between `boot_inflation_rate_min` and `boot_inflation_rate_max`.
In case of inflation is higher than the `boot_inflation_rate_max` param, the inflation sets as
`boot_inflation_rate_max`. In case of inflation lower than `boot_inflation_rate_min` param the inflation sets as
`boot_inflation_rate_min`.

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

Agents (neurons) delegate liquid BOOT to heroes, and they mint corresponding amounts of Hydrogen (H).

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}\Delta hydrogen\_supply = \Delta boot\_bonded\_supply"></p>

We model `boot_bonded_supply` using the next formula:

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}boot\_bonded\_supply_t = boot\_bonded\_supply_{t-1} %2B \Delta boot\_bonded\_supply"></p>

where:

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}\Delta boot\_bonded\_supply = (boot\_bonded\_share\_limit - boot\_bonded\_share_{t-1}) \cdot boot\_supply_{t-1} \cdot bonding\_speed\_coeff"></p>

We model neurons bonding behavior using parameters `boot_bonding_share_limit` `(0.85)` and `bonding_speed_coeff`
`(0.01)`, where `boot_bonding_share_limit` is the ratio between `boot_bonded_supply` and `boot_supply` which
neurons tend to have. And `bonding_speed_coeff` is the speed of bonding every timestep.

The one share of minted H tokens stays in the liquid state, another one is used for minting resource tokens (A
and V). `hydrogen_liquid_ratio` parameter is used in the current model which describes the token share allocated
to liquid H. The rest tokens are used for minting A and V in `hydrogen_liquid_ratio`.  

![H Supply](images/h_supply.png)

### Initial Values

- `boot_bonded_supply` `(10e12)`
- `hydrogen_supply` `(10e12)`

### Simulation Parameters

- `boot_bonding_share` `(0.8)`
- `hydrogen_liquid_ratio` `(0.2)`
- `boot_bonding_share_limit` `(0.85)`
- `bonding_speed_coeff` `(0.01)`
- `ampere_volt_ratio` `(0.5)`

## Gift Claim Dynamics

The addresses for gifts are defined in the [research](https://github.com/Snedashkovsky/cybergift). This research 
[concludes](https://github.com/Snedashkovsky/cybergift#prize-to-be-the-first) 6M addresses for distribution of 70% of 
BOOT tokens.

The `boot_claimed_supply` function has two phases:

- before `days_for_gift_activation`
- after `days_for_gift_activation`

It's expected that `claimed_at_activation_share` * `boot_gift_amount_init` amount of BOOTs will be reached in
`days_for_gift_activation`. After that, (1 - `claimed_at_activation_share`) * `boot_gift_amount_init` should be claimed
in `days_for_gift_full_claim`.

Therefore, the `boot_claimed_supply` function can be defined as linear function with condition:

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}boot\_claimed\_supply_t = boot\_claimed\_supply_{t-1} %2B \Delta boot\_claimed\_supply"></p>

if `t` < `days_for_gift_activation`:

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}\Delta boot\_claimed\_supply = \frac{claimed\_at\_activation\_share \cdot boot\_gift\_amount\_init}{days\_for\_gift\_activation}"></p>

if `t` = `days_for_gift_activation`

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}\Delta boot\_claimed\_supply = boot\_gift\_amount\_init \cdot 0.1"></p>

if `t` > `days_for_gift_activation`:

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}\Delta boot\_claimed\_supply = boot\_gift\_amount\_init \cdot 0.01"></p>


### `boot_to_distribution_supply`

In case where tokens have already been claimed but not transferred they change their state to “to_distribution” state 
(ready to be transferred to neurons). 


<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green} boot\_to\_distribution\_supply_t = boot\_to\_distribution\_supply_{t-1} %2B \Delta boot\_claimed\_supply %2B \Delta boot\_frozen\_supply"></p>

### `boot_frozen_supply`

The `boot_frozen_supply` is defined as the token amount on the gift contract balance. 

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green} boot\_frozen\_supply_t = boot\_frozen\_supply_{t-1} %2B \Delta boot\_frozen\_supply"></p>

Therefore, the `delta_boot_frozen_supply` function can be represented in 3 phases:

if `t` < `days_for_gift_activation`:

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green} \Delta boot\_frozen\_supply = 0"></p>

if `t` >= `days_for_gift_activation`:

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green} \Delta boot\_frozen\_supply = -boot\_to\_distribution\_supply_{t-1} \cdot 0.1"></p>

Assumptions:

- neurons (`agents_count_at_activation`) will claim our gift. After that the gift will be activated
- it will take `days_for_gift_activation` since genesis before the gift claiming process will be completed
- neurons on the moment of gift activation will claim share of the gift (`claimed_at_activation_share`)
- claim process can be prolonged on `days_for_gift_full_claim` in case if `agents_count_at_activation` will not
  reach the target goal by `days_for_gift_activation`

### Initial Values

- `boot_frozen_supply` `(700e12)`
- `boot_claimed_supply` `(0)`
- `boot_to_distribution_supply` `(0)`

### Simulation Parameters

- `days_for_gift_activation` `(30)`
- `claimed_at_activation_share` `(0.85)`
- `days_for_gift_full_claim` `(150)`
- `agents_count_at_activation` `(10'000, 50'000, 100'000)`
- `boot_gift_amount_init` `(700e12)`

## Understanding Network Effects

### Agents (Neurons) Growth

To model agents' growth dynamics of the Bostrom network, we did a regression analysis on ETH active addresses
dynamics ([excel spreadsheet online](https://needfordata-my.sharepoint.com/:x:/g/personal/max_needfordata_ru/EZWCgmE-VOBEsGJTg8lslpYBP2LQoBFdMC9LgXleJ3Dj_Q?e=PwmaIh)).
We calculated [ethereum active addresses](eth_active_agents.ipynb) as addresses with a balance more than 0.01 ETH
(the balance sufficient to complete at least 1 transaction).

![Dynamics of Ethereum Addresses](images/eth_active_addresses_regression.png)

We have combined 2 trend lines and derived the following formula of addresses counting by days from ETH dynamics.

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}agents\_count = 2 \cdot days^{2} %2B 100 \cdot days %2B 8700"></p>

Assuming that there are much more crypto-agents now than there were at the time of ETH launch, we adjusted the
formula with coefficients to expect more rapid growth.

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}agents\_count = 9 \cdot days^2 %2B 100 \cdot days %2B agents\_count\_at\_activation"></p>

![Neurons Forecast](images/neurons_forecast.png)

### Capitalization Dynamics

We decided to model total `capitalization_in_eth` through `capitalization_per_agent` metric derived from ETH
capitalization in BTC (from the 100-th day from start till 2160 days of the network, as on the first 100 days ETH
price in BTC had a lot of fluctuations).

![Ethereum Capitalization per Active Addresses in BTC](images/eth_cap_per_active_address_in_btc_regression.png)

We derived such formula:

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}capitalization\_per\_agent\_eth\_network = 60\,000 \cdot agents\_count^{-0.7}"></p>

We assumed that the dynamics of capitalization of BOOT token in ETH will resemble ETH token capitalization
dynamics in BTC prices. We adjusted the formula that our first-day `capitalization_per_agent` will be equal to 32
ETH (`capitalization_per_agent`).

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}capitalization\_per\_agent = start\_capitalization\_per\_agent \cdot agents\_count\_at\_activation^{0.7} \cdot agents\_count^{-0.7}"></p>

![BOOT Capitalization](images/boot_capitalization.png)

### Initial Values

- `capitalization_per_agent` `(32)`
- `agents_count` `(750)`

### Simulation Parameters

- `agents_count_at_activation` `(100'000)`


## Capitalization and Price

`capitalization_in_eth` in ETH is defined by the formula:

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}capitalization\_in\_eth_{t} = agents\_count_{t} \cdot capitalization\_per\_agent_{t}"></p>

`gboot_price` (Giga BOOT) price in ETH is defined by the formula:

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}gboot\_price_t = \frac{capitalization\_in\_eth_t}{boot\_supply_t \cdot 1e9}"></p>

![Validators Revenue](images/validators_revenue.png)

## Predicting V Demand

V are natural tokens. Each V enables its holder to produce 1 cyberlink daily. To simulate cyberlinks usage we
have derived base estimate of `cyberlinks_per_day` formula from ETH data:

![ETH Data](images/eth_transactions_per_active_address_regression.png)

We derived such formula:

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}transactions\_per\_agent = 9 \cdot agents\_count^{-0.3}"></p>

And we adjusted such a formula by multiplication coefficient (`cyberlinks_trasactions_coeff`) because we expect
that neurons in the BOSTROM network will be more active than agents in ETH. Also, we adjusted such a formula by
adding a number of `extra_links` and `guaranteed_links`.

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}cyberlinks\_per\_day = 9 \cdot cyberlinks\_trasactions\_coeff \cdot agents\_count^{-0.3} %2B extra\_links %2B guaranteed\_links"></p>


**NOT IMPLEMENTED!!!**
`extra_links` count depends on UX specifics, such as setting the name of a neuron, following (proportion of
neurons) and extra:

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}extra\_links ~ f( agents\_count, setting name, following, extra )">

Also, the founding team envisions some basic stuff to cyberlink such as naming systems and tokens. So we can rely
on this demand too. We left `guaranteed_links` count equal to 0 but it can be changed in the future.

![cyberLinks Forecast](images/cyberlinks_forecast.png)

### Simulation Parameters

- `cyberlinks_trasactions_coeff` `(15)`
- `extra_links` `(0)`
- `guaranteed_links` `(0)`

## Adjusting A and V Supply

System designed in the way that investminted `volt_base_investmint_amount` for `volt_base_investmint_period`
yields 1 V.

System designed in the way that investminted `ampere_base_investmint_amount` for `ampere_base_investmint_period`
yields 1 A.

`ampere_base_investmint_period`, `volt_base_investmint_period` - are periods of investminting H token for the
selected token (A or V) by the current neuron. These periods are chosen by neurons themselves according to their
understanding and priorities of maximizing their benefits.

`ampere_base_investmint_period`, `volt_base_investmint_period` are limited by the `investmint_max_period` system
setting, which has the dynamic formula written below.

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}investmint\_max\_period_t = horizon\_period\_init \cdot {\lceil{\frac{t}{horizon\_period\_init}}\rceil}"></p>

Where `horizon_period_init` is the period before first `investmint_max_period` raise.

`ampere_base_halving_period`, `volt_base_halving_period` - time period to decrease mint_rate variable.

`ampere_mint_rate`, `volt_mint_rate` are coefficients that regulate the amount of minted resource tokens A and V.
They are set at the beginning and further these coefficients are halved each `ampere_base_halving_period`,
`volt_base_halving_period` accordingly.

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}{ampere\_mint\_rate_t} = 2^{-\lfloor{\frac{t}{ampere\_base\_halving\_period}}\rfloor}"></p>


<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}{volt\_mint\_rate_t} = 2^{-\lfloor{\frac{t}{volt\_base\_halving\_period}}\rfloor}"></p>

`ampere_mint_rate`, `volt_mint_rate` are limited by - `ampere_mint_rate_min`, `volt_mint_rate_min` parameters.

As Ampere (A) are resource tokens, and they do not have natural measures we decided to model A supply equal to V.


![A Halving Cycles](images/a_halving_cycles.png)
![V Halving Cycles](images/v_halving_cycles.png)


### Initial Values

- `ampere_mint_rate` `(1)`
- `volt_mint_rate` `(1)`
- `investmint_max_period` `(547)`


### Simulation Parameters

- `ampere_base_halving_period` `(547)`
- `volt_base_halving_period` `(547)`
- `ampere_mint_rate_min` `(0.01)`
- `volt_mint_rate_min` `(0.01)`
- `investmint_max_period_init` `(547)`
- `horizon_period_init` `(547)`

## A and V Minting

A are minted according to the following formula:

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}{ampere\_minted\_amount} = \lfloor{\frac{hydrogen\_investmint\_amount}{ampere\_base\_investmint\_amount} \cdot \frac{investmint\_period}{ampere\_base\_investmint\_period} \cdot ampere\_mint\_rate}\rfloor"></p>

V are minted according to the following formula:

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}{volt\_minted\_amount} = \lfloor{\frac{hydrogen\_investmint\_amount}{volt\_base\_investmint\_amount} \cdot \frac{investmint\_period}{volt\_base\_investmint\_period} \cdot volt\_mint\_rate}\rfloor"></p>

In the model it is implemented as:

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}hydrogen\_for\_investminting = (\Delta hydrogen\_supply \cdot (1 - hydrogen\_liquid\_ratio)) %2B released\_hydrogen"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}hydrogen\_for\_ampere\_investminting = hydrogen\_for\_investminting \cdot ampere\_volt\_ratio"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}hydrogen\_for\_volt\_investminting = hydrogen\_for\_investminting \cdot (1-ampere\_volt\_ratio)"></p>

So we can rephrase formulas as:

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}{ampere\_minted\_amount_{t}} = \lfloor{\frac{hydrogen\_for\_ampere\_investminting_{t}}{ampere\_base\_investmint\_amount} \cdot \frac{investmint\_max\_period_{t-1} \cdot investmint\_period\_share }{ampere\_base\_investmint\_period} \cdot ampere\_mint\_rate_{t-1}}\rfloor"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}{volt\_minted\_amount_{t}} = \lfloor{\frac{hydrogen\_for\_volt\_investminting_{t-1}}{volt\_base\_investmint\_amount} \cdot \frac{investmint\_max\_period_{t} \cdot investmint\_period\_share }{volt\_base\_investmint\_period} \cdot volt\_mint\_rate_{t-1}}\rfloor"></p>

We assume that `investmint_period_share` * `investmint_max_period` is an average period for investminting per neuron. 

`investmint_period_share` has stohastic function representation with u = 0.5, sigma = 0.1.

![A Supply](images/a_supply.png)
![V Supply](images/v_supply.png)

### Simulation Parameters

- `investmint_period_share` `(N(0.5, 0.01))`
- `ampere_volt_ratio` `(0.5)`
- `ampere_base_investmint_amount` `(100'000'000)`
- `volt_base_investmint_amount` `(1'000'000'000)`
- `ampere_base_investmint_period` `(30)`
- `volt_base_investmint_period` `(30)`



## Planing GPU Memory Usage

We had stress testing on the testnet to measure resources usage.

|                   | Bostrom Testnet 4 |      1B links |      100B links |
| :---------------- | ----------------: | ------------: | --------------: |
| Cyberlinks        |        40'335'720 | 1'000'000'000 | 100'000'000'000 |
| TPS               |                10 |            50 |             730 |
| GPU RAM Usage, GB |                 2 |            46 |           4'562 |
| GPU Time Usage, s |                35 |           900 |          90'000 |
| CPU RAM Usage, GB |                48 |         1'200 |         120'000 |
| CPU Time Usage, s |              0.10 |             2 |             250 |

The number of transactions per second is the main indicator of the load on the system. We have chosen to calculate this indicator taking into account only the number of cyberlinks. 

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}transactions\_per\_second=\frac{cyberlinks\_per\_day}{24 \cdot 3600} " ></p>

According to stress testing measurements on testnet we derived formulas for GPU memory usage, CPU memory usage,
GPU time usage and CPU time usage:

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}gpu\_memory\_usage_t=40 \cdot cyberlinks\_count_{t-1} %2B 40 \cdot particles_{t-1}" ></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}cpu\_memory\_usage_t=1.2 \cdot 10^{3} \cdot cyberlinks\_count_{t-1}" ></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}cpu\_time\_usage_t=2.5 \cdot 10^{-9} \cdot cyberlinks\_count_{t-1}" ></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}gpu\_time\_usage_t=9 \cdot 10^{-7} \cdot cyberlinks\_count_{t-1}" ></p>

where:

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}particles_{t-1}=cyberlinks\_count_{t-1} \cdot particle\_per\_link" ></p>

The `particle_per_link` parameter defines amount of particles per cyberlink.


![Transactions per seconds](images/transactions_per_second.png)
![GPU Memory and Time Usage](images/memory_and_time_usage.png)

### Initial Values

- `gpu_memory_usage` `(0)`
- `cpu_memory_usage` `(0)`
- `cpu_time_usage` `(0)`
- `gpu_time_usage` `(0)`


### Simulation Parameters

- `particle_per_link` `(0.1)`


## Investments into Infrastructure

Further we can estimate revenue of 1 validator in ETH Equivalent, given that all validators have
commission (`validator_commission`) equals `validator_commission` and that there are `max_validator_count`
validators.

`validator_revenue_gboot` is defined by formula:

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}validator\_revenue\_gboot_t = \frac{timestep\_provision\_boot_{t-1} \cdot validator\_commission \cdot gboot\_price_{t-1}}{ max\_validator\_count} "></p>


### Simulation parameters

- `validator_commission` `(0.1)`
- `max_validator_count` `(92)`


## Mathematical Specification

### Initial Values

- `boot_supply` `(1e15)`
- `boot_inflation_rate` `(0.05)`

- `boot_bonded_supply` `(10e12)`
- `hydrogen_supply` `(10e12)`

- `boot_frozen_supply` `(700e12)`
- `boot_claimed_supply` `(0)`
- `boot_to_distribution_supply` `(0)`

- `capitalization_per_agent` `(32)`
- `agents_count` `(750)`

- `ampere_mint_rate` `(1)`
- `volt_mint_rate` `(1)`
- `investmint_max_period` `(547)`

- `gpu_memory_usage` `(0)`
- `cpu_memory_usage` `(0)`
- `cpu_time_usage` `(0)`
- `gpu_time_usage` `(0)`

### Summary of Simulation Parameters


- `timesteps_per_year` `(365)`
- `sim_period` `(10)`

- `boot_inflation_rate_max`  `(0.15)`
- `boot_inflation_rate_min`  `(0.03)`
- `boot_bonded_share_target` `(0.80)`
- `boot_inflation_rate_change_annual_annual`  `(0.20)`

- `boot_bonding_share` `(0.8)`
- `hydrogen_liquid_ratio` `(0.2)`
- `boot_bonding_share_limit` `(0.85)`
- `bonding_speed_coeff` `(0.01)`
- `ampere_volt_ratio` `(0.5)`

- `days_for_gift_activation` `(30)`
- `claimed_at_activation_share` `(0.85)`
- `days_for_gift_full_claim` `(150)`
- `agents_count_at_activation` `(100'000)`
- `boot_gift_amount_init` `(700e12)`

- `agents_count_at_activation` `(100'000)`

- `cyberlinks_trasactions_coeff` `(15)`
- `extra_links` `(0)`
- `guaranteed_links` `(0)`

- `ampere_base_halving_period` `(547)`
- `volt_base_halving_period` `(547)`
- `ampere_mint_rate_min` `(0.01)`
- `volt_mint_rate_min` `(0.01)`
- `investmint_max_period_init` `(547)`
- `horizon_period_init` `(547)`

- `investmint_period_share` `(N(0.5, 0.01))`
- `ampere_volt_ratio` `(0.5)`
- `ampere_base_investmint_amount` `(100'000'000)`
- `volt_base_investmint_amount` `(1'000'000'000)`
- `ampere_base_investmint_period` `(30)`
- `volt_base_investmint_period` `(30)`

- `particle_per_link` `(0.1)`

- `validator_commission` `(0.1)`
- `max_validator_count` `(92)`


### Formulas used as it is:

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}capitalization\_in\_eth_t = agents\_count_{t-1} \cdot capitalization\_per\_agent_{t-1}"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}gboot\_price_t=\frac{capitalization\_in\_eth_{t-1}}{boot\_supply_{t-1}}"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}validator\_revenue\_gboot_t = \frac{timestep\_provision\_boot_{t-1} \cdot validator\_commission \cdot gboot\_price_{t-1}}{ max\_validator\_count} "></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}{ampere\_mint\_rate_t} = 2^{-\lfloor{\frac{t}{ampere\_base\_halving\_period}\rfloor}}"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}{volt\_mint\_rate_t} = 2^{-\lfloor{\frac{t}{volt\_base\_halving\_period}\rfloor}}"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}investmint\_max\_period_t = horizon\_period\_init \cdot {\lceil{\frac{t}{horizon\_period\_init}}\rceil}"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}transactions\_per\_second_t=\frac{cyberlinks\_per\_day_t}{24 \cdot 3600} " ></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}gpu\_memory\_usage_t=40 \cdot cyberlinks\_count_{t-1} %2B 40 \cdot particles_{t-1}" ></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}cpu\_memory\_usage_t=1.2 \cdot 10^{3} \cdot cyberlinks\_count_{t-1}" ></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}cpu\_time\_usage_t=2.5 \cdot 10^{-9} \cdot cyberlinks\_count_{t-1}" ></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}gpu\_time\_usage_t=9 \cdot 10^{-7} \cdot cyberlinks\_count_{t-1}" ></p>

where:

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}particles_{t-1}=cyberlinks\_count_{t-1} \cdot particle\_per\_link" ></p>


### Formulas for Differential Equations: (Считаю эту секцию бесполезной! пока закомментировал)

<!-- <p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}t = \frac{timesteps\_per\_year}{365}"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}boot\_bonded\_share_t = \frac{boot\_bonded\_supply_{t-1}}{boot\_supply}"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}boot\_inflation\_rate\_change\_annual_t = \frac{1 - \frac{boot\_bonded\_share_{t-1}}{boot\_bonded\_share\_target}}{boot\_inflation\_rate\_change\_annual}"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}boot\_inflation\_rate\_change_t = \frac{boot\_inflation\_rate\_change\_annual_t}{timesteps\_per\_year}"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}boot\_inflation\_rate_t = boot\_inflation\_rate_{t-1} + %2B boot\_inflation\_rate\_change"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}hydrogen\_supply = boot\_liquid\_supply \cdot boot\_bonded\_share\_current"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}agents\_count = 9 \cdot days^2 %2B 100 \cdot days %2B agents\_count\_at\_activation"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}transactions\_per\_agent = 9 \cdot agents\_count^{-0.3}"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}cyberlinks\_per\_day = 9 \cdot agents\_count^{-0.3} %2B extra\_links %2B guaranteed\_links"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}extra\_links ~ f( agents\_count, name, following, extra)">

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}claim(timestep) = 7 \cdot 10^{14} \cdot e^{-0.0648637 \cdot timestep}"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}{ampere\_minted\_amount} = \lfloor{\frac{hydrogen\_supply}{ampere\_base\_investmint\_amount} \cdot \frac{investmint\_period}{ampere\_base\_investmint\_period} \cdot ampere\_mint\_rate}\rfloor"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}{volt\_minted\_amount} = \lfloor{\frac{hydrogen\_supply}{volt\_base\_investmint\_amount} \cdot \frac{investmint\_period}{volt\_base\_investmint\_period} \cdot volt\_mint\_rate}\rfloor"></p> -->



### Differential Equations

- `boot_supply` - the supply of BOOT token
- `boot_inflation_rate` - inflation on timesep
- `boot_bonded_supply` - bonded (staked) network token amount (H Supply)
- `hydrogen_supply` - the supply of H token
- `hydrogen_liquid_supply` - liquid supply of H
- `boot_claimed_supply` - claimed from contract BOOT amount
- `boot_frozen_supply` - not claimed (frozen) network token amount
- `boot_liquid_supply` - liquid network token amount
- `boot_to_distribution_supply` - ready to transfer claimed BOOT amount
- `agents_count` - the amount of the active neurons
- `capitalization_per_agent` - the value of neuron in ETH
- `cyberlinks_count` - number of cyberlinks
- `ampere_supply` - A resource token amount
- `volt_supply` - V token amount

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}boot\_supply_t = boot\_supply_{t-1} %2B timestep\_provision\_boot_t"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}boot\_inflation\_rate_t = boot\_inflation\_rate_{t-1} + %2B boot\_inflation\_rate\_change"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}boot\_bonded\_supply_t = boot\_bonded\_supply_{t-1} %2B {\Delta boot\_bonded\_supply}"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}hydrogen\_supply_t = hydrogen\_supply_{t-1} %2B {\Delta hydrogen\_supply}"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}hydrogen\_liquid\_supply_t = hydrogen\_liquid\_supply_{t-1} %2B {\Delta hydrogen\_liquid\_supply\_supply}"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}boot\_claimed\_supply_t = boot\_claimed\_supply_{t-1} %2B \Delta boot\_claimed\_supply"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green} boot\_frozen\_supply_t = - boot\_frozen\_supply_{t-1} %2B \Delta boot\_frozen\_supply"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}boot\_liquid\_supply_t = boot\_liquid\_supply_{t-1} %2B timestep\_provision\_boot_t - {\Delta boot\_frozen\_supply} - {\Delta boot\_bonded\_supply}"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green} boot\_to\_distribution\_supply_t = boot\_to\_distribution\_supply_{t-1} %2B \Delta boot\_claimed\_supply %2B \Delta boot\_frozen\_supply"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}agents\_count_t = agents\_count_{t-1} %2B {\Delta agents\_count}"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}capitalization\_per\_agent_t = capitalization\_per\_agent_{t-1} %2B {\Delta capitalization\_per\_agent}"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}cyberlinks\_count_{t} = cyberlinks\_count_{t-1} %2B {\Delta cyberlinks\_count}"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}ampere\_supply_t = ampere\_supply_{t-1} %2B {\Delta ampere\_supply}"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}volt\_supply_t = volt\_supply_{t-1} %2B {\Delta volt\_supply}"></p>


where the rate of change (<img src="https://render.githubusercontent.com/render/math?math=\color{green}\Delta">) is:

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}timestep\_provision\_boot_t = \frac{boot\_supply_{t-1} \cdot boot\_inflation\_rate_{t}}{timesteps\_per\_year}"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}boot\_inflation\_rate\_change = \frac {({1 - \frac{boot\_bonded\_share_{t-1}}{boot\_bonded\_share\_target}}) \cdot{boot\_inflation\_rate\_change\_annual}}{timesteps\_per\_year}"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}\Delta boot\_bonded\_supply = (boot\_bonded\_share\_limit - boot\_bonded\_share_{t-1}) \cdot boot\_supply_{t-1} \cdot bonding\_speed\_coeff"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}\Delta hydrogen\_supply = \Delta boot\_bonded\_supply"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}{\Delta hydrogen\_liquid\_supply\_supply} = \Delta hydrogen\_supply \cdot hydrogen\_liquid\_ratio"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}\Delta boot\_claimed\_supply = \frac{claimed\_at\_activation\_share \cdot boot\_gift\_amount\_init}{days\_for\_gift\_activation}"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green} \Delta boot\_frozen\_supply = - boot\_to\_distribution\_supply_{t-1} \cdot 0.1"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}{\Delta agents\_count} = 18 \cdot t %2B 100"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}{\Delta capitalization\_per\_agent} = 2990 \cdot (-0.7) \cdot agents\_count_{t-1}^{-1.7} \cdot \Delta agents\_count"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}{\Delta cyberlinks\_count} = 9 \cdot cyberlinks\_transaction\_coeff \cdot agents\_count_{t-1}^{-0.3} %2B extra\_links %2B guaranteed\_links" ></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}{\Delta ampere\_supply} = \lfloor{\frac{hydrogen\_for\_ampere\_investminting_{t-1}}{ampere\_base\_investmint\_amount} \cdot \frac{investmint\_max\_period_{t} \cdot investmint\_period\_share }{ampere\_base\_investmint\_period} \cdot ampere\_mint\_rate_{t-1}}\rfloor"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}{\Delta volt\_supply} = \lfloor{\frac{hydrogen\_for\_volt\_investminting_{t-1}}{volt\_base\_investmint\_amount} \cdot \frac{investmint\_max\_period_{t} \cdot investmint\_period\_share }{volt\_base\_investmint\_period} \cdot volt\_mint\_rate_{t-1}}\rfloor"></p>

where:

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}boot\_bonded\_share_{t} = \frac{boot\_bonded\_supply_{t-1}}{boot\_supply_{t-1}}"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}hydrogen\_for\_ampere\_investminting_t = hydrogen\_for\_investminting_{t-1} \cdot ampere\_volt\_ratio"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}hydrogen\_for\_volt\_investminting_t = hydrogen\_for\_investminting_{t-1} \cdot (1-ampere\_volt\_ratio)"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}hydrogen\_for\_investminting_t = (\Delta hydrogen\_supply \cdot (1 - hydrogen\_liquid\_ratio)) %2B released\_hydrogen_t"></p>


## Conclusions

![BOOT Supply and Inflation Rate](images/boot_supply.png)
![Validators Revenue](images/validators_revenue.png)
![Demand and Supply of cyberLinks](images/demand_and_supply_of_cyberlinks.png)
