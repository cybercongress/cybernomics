<!-- хаки рендеринга latex https://gist.github.com/a-rodin/fef3f543412d6e1ec5b6cf55bf197d7b#gistcomment-3523272 -->
# Bostrom network simulation

## Usage

0. Install Python3 if you have no
1. Go to `bostrom_simulation` folder
```bash
cd bostrom_simulation
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

7. On the top bar `Kernel`->`Restart & Run All`

8. The simulation time depends on the simulation period you have set, f.e. for 7 years it approximately 1 hour

9. Look at the results and conclude.

## Goals

To optimize parameters for launching Bostrom.

An idea is to model the value of BOOT through the understanding of established network effects in Ethereum.
Then we can forecast claim dynamics and address growth based on approximated network effects. Assuming some demand for cyberlinks based on address growth we can adjust the supply of cyberlinks so that V price could grow. The given model also allows defining inflation parameters of BOOT to optimize investments into the hardware infrastructure.

## Timestpep unit

The timestepp variable for simulation defined as `timestep` and depends on `timesteps_per_year` param. 

timesteps_per_year == 365
timestep == day

## BOOT supply 

Simulate the ability of heroes to invest in infrastructure depending on different market conditions.  

The fomula is described in [Differential Equations](#differential-equations) section.

### BOOT inflation

The minting mechanism was designed to:

- allow for a flexible inflation rate determined by market demand targeting a particular bonded-stake ratio
- effect a balance between market liquidity and staked supply

In order to best determine the appropriate market rate for inflation rewards, a moving change rate is used. The moving change rate mechanism ensures that if the % bonded is either over or under the goal %-bonded, the inflation rate will adjust to further incentivize or disincentivize being bonded, respectively. Setting the goal %-bonded at less than 100% encourages the network to maintain some non-staked tokens which should help provide some liquidity.

It can be broken down in the following way:

- If the inflation rate is below the `boot_bonded_share_target` the inflation rate will increase until a maximum value (`boot_inflation_max`) is reached
- If the `boot_bonded_share_target` (0.70 in bostrom network) is maintained, then the inflation rate will stay constant
- If the inflation rate is above the goal `boot_bonded_share_target` the inflation rate will decrease until a minimum value (`boot_inflation_min`) is reached

The target annual inflation rate is recalculated each `timestep`. The inflation is also subject to a rate change (positive or negative) depending on the distance from the desired ratio (0.70). The maximum rate change possible is defined to be `boot_inflation_rate_change` per year, however the annual inflation is capped as between `boot_inflation_min` and `boot_inflation_max`.

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}boot\_inflation\_rate_t = boot\_inflation\_rate_{t-1} %2B {\Delta boot\_inflation\_rate}"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}timestep\_provision_{t-1} = \frac{boot\_supply_{t-1} \cdot boot\_inflation\_rate\_change{t-1}}{timesteps\_per\_year}"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}vested\_ratio_{t-1} = \frac{vested\_boot}{boot\_supply}"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}{investmint\_max\_period_t = investmint\_max\_period\_init \cdot 2^{\lfloor{\frac{t}{timesteps\_per\_year}}\rfloor}}"></p>

### Simulation parameters

- __*start_boot_supply*__ `(1e15)`
- __*boot_inflation_rate_change_annual*__  `(0.07)`
- __*boot_inflation_max*__  `(0.20)`
- __*boot_inflation_min*__  `(0.05)`
- __*boot_bonded_share_target*__ `(0.70)` 
<!-- - __*boot_supply*__   -->

## Modeling H supply

Agents will delegate __*boot_bonded_share*__ (70%) of BOOT Supply to heroes, and H will be minted in the corresponding amount.

<img src="https://render.githubusercontent.com/render/math?math=\color{green}h\_supply = boot\_supply \cdot boot\_bonded\_share">

### Simulation parameters

- __*boot_bonded_share*__ `(0.7)`
- <img src="https://render.githubusercontent.com/render/math?math=\color{green}h\_supply = boot\_supply \cdot boot\_bonded\_share">


## Gift claim dynamics
 
The addresses for gift are defined in the [research](https://github.com/Snedashkovsky/cybergift). This research [concludes](https://github.com/Snedashkovsky/cybergift#prize-to-be-the-first) 6M addresses for distribution of 70% of BOOT tokens. Further we need to model how this gifts can be claimed. 

We need to derive __*claim_rate*__ (by formula to define).

Assumptions:
- agents (__*agents_count_at_activation*__) will claim our gift. After that the gift will be activated 
- it will take __*days_for_gift_activation*__ since genesis before the gift claiming process will be completed 
- agents on the moment of gift activation will claim share of the gift (__*claimed_at_activation_share*__)
- claim process can be prolonged on __*days_for_gift_full_claim*__ in case if __*agents_count_at_activation*__ will not reach the target goal by __*days_for_gift_activation*__.
- __*liquid_boot_supply_share*__ - is share of BOOT supply that will be in circulation from the network launch

After the modeling of claim dynamics, we can set baselines for adoption ("understanding network effects" chapter).

### Simulation parameters

- __*agents_count_at_activation*__ `(10'000, 50'000, 100'000)`
- __*days_for_gift_activation*__ `(100, 150)`
- __*days_for_gift_full_claim*__ `(0, 360)` 
- __*claimed_at_activation_share*__ `(1, 0.5)`
- __*liquid_boot_supply_share*__ `(0.25)`
- __*claimed_boot_supply*__ - ?

## Understanding network effects

Modeling price of BOOT as a function of usage weighted on network effects.  

To model agents' growth dynamics of the Bostrom network, we did a regression analysis on ETH active agent dynamics
([excel spreadsheet online](https://needfordata-my.sharepoint.com/:x:/g/personal/max_needfordata_ru/EZWCgmE-VOBEsGJTg8lslpYBP2LQoBFdMC9LgXleJ3Dj_Q?e=PwmaIh)).
We calculated [ethereum active agents](eth_active_agents.ipynb) as addresses with a balance more than 0.01 ETH (the
balance sufficient to complete at least 1 transaction).

![](images/EthAgentsDynamics.png)

We have combined 2 trendlines and derived the following formula of agents count by days from ETH dynamics.

<img src="https://render.githubusercontent.com/render/math?math=\color{green}agents\_count = 2 \cdot days^{2} %2B 100 \cdot days %2B 8700">

Assuming that there are much more crypto-agents now than it was on  time of ETH launch we adjusted formula with
coeffients to expect more rapid growth.

<img src="https://render.githubusercontent.com/render/math?math=\color{green}agents\_count = 9 \cdot days^2 %2B 100 \cdot days %2B agents\_count\_at\_activation">

We decided to model total capitalization through __*capitalization_per_agent*__ metric derived from ETH capitalization in
BTC (from 100 day from start till 2160 days of network, as before 100 days ETH price in BTC had a lot of fluctuations).

![ETH dynamics](images/EthCapPerAgentActiveInBTC1.png)

We derived such formula:

<img src="https://render.githubusercontent.com/render/math?math=\color{green}capitalization\_per\_agent = 60\,000 \cdot agents\_count^{-0.7}">


We assumed that dynamics of capitalization of BOOT token in ETH will resemble ETH token dynamics in BTC prices.
We adjusted the formula that our first day __*capitalization_per_agent*__ will be equal to 1 ETH
(__*start_capitalization_per_agent*__).

<img src="https://render.githubusercontent.com/render/math?math=\color{green}capitalization\_per\_agent = start\_capitalization\_per\_agent \cdot agents\_count\_at\_activation^{0.7} \cdot  agents\_count^{-0.7}">

### Simulation parameters

- <img src="https://render.githubusercontent.com/render/math?math=\color{green}agents\_count = 9 \cdot days^2 %2B 100 \cdot days %2B agents\_count\_at\_activation">
- __*start_capitalization_per_agent*__ `(1)`
- <img src="https://render.githubusercontent.com/render/math?math=\color{green}capitalization\_per\_agent = start\_capitalization\_per\_agent \cdot agents\_count\_at\_activation^{0.7} \cdot  agents\_count^{-0.7}">


## Predicting V demand

Simulate cyberlinks usage.  

We have derived base estimate of cyberlink per agent formula from ETH data:

![ETH Data](images/EthAgentsCountActive_vs_EthTransPerAgent.png)

We derived such formula:

<img src="https://render.githubusercontent.com/render/math?math=\color{green}transactions\_per\_agent = 9 \cdot agents\_count^{-0.3}">

And we adjust such formula with the number of extra links and guaranteed links. 

<img src="https://render.githubusercontent.com/render/math?math=\color{green}cyberlinks\_per\_agent = 9 \cdot agents\_count^{-0.3} %2B extra\_links %2B guaranteed\_links">

*Extra_links*__ count depends on UX specifics, such as name setting, following (proportion of agents) and extra:

<img src="https://render.githubusercontent.com/render/math?math=\color{green}extra\_links ~ f( agents\_count, name, following, extra)"> 

Also, the founding team envisions some basic stuff to cyberlink such as naming systems and tokens. So we can rely
on this demand also adding __*guaranteed_links*__ count.

### Simulation parameters 

- __*extra_links*__ - function to define
- __*guaranteed_links*__ - function to define
- <img src="https://render.githubusercontent.com/render/math?math=\color{green}cyberlinks\_per\_agent = 9 \cdot agents\_count^{-0.3} %2B extra\_links %2B guaranteed\_links">

## Adjusting V and A supply

To model minting properties of V for the planning of GPU storage and maximization of price. As A reource do not have natural measure we decide to model A supply rules equal to V. 

Gboot __*__ 1 day = 1 volt

__*investmint_period*__ - is period of investminiting H token for selected agent. It is choosen by agent according to his understanding and priorities of maximisation his benefits. 


And it is limited by system setting of __*investmint_max_period*__, that has some dynamic formula to define and research (presumably it will become longer with the age of network - [3, 6, 9, 12 ... ] monthes but no longer than the time from network start). 
- __*investmint_amount*__ - is amount of H token investminted by agents for selected period of time.  
- __*halving_time*__ - time period to increase investmint amount twofold.
- __*a_v_ratio*__ - ?

### Simulation parameteres

Parameters to define for V and A:
- __*base_investmint_preiod_amper*__  `(timesteps_per_year / 12)`
- __*base_investmint_preiod_volt*__  `(timesteps_per_year / 12)`
- __*base_investmint_amount_amper*__  `(100_000_000)`
- __*base_investmint_amount_volt*__  `(100_000_000)`
- __*investmint_max_period_init*__ `(timesteps_per_year / 12)`  
- __*horizont_step*__ ?
- __*base_halving_period_amper*__ `(12_000_000 * 6.4)`
- __*base_halving_period_volt*__ `(12_000_000 * 6.4)`
- __*a_v_ratio*__ `(0.5)`  

## Investments into infrastructure

- BOOT Supply
- BOOT Staked
- Comission = 10%
- BOOT price
- Validator count = 92
 
Target goal of simulation is to estimate revenue of 1 validator.

## Claim function

The function of claim frozen tokens is:

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}claim(timestep) = 7 \cdot 10^{14} \cdot e^{-0.0648637timestep}"></p>

![calim](images/claim.png)

<!-- <img src='images/claim.png' /> -->

## Vesting and Unvesting

The vesting function is defined as the amount of locking tokens in the time unit assumed by all liquid tokens must be
locked in the lock timeframe.

The unvesting function is defined as the amount of unlocking tokens in the time unit assumed by all locked tokens must
be unlocked in the unlock timeframe.

## Amper minting

Amperes mints by the following formula:

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}{amper} = \lfloor{\frac{hydrogent}{base\_investmint\_amount\_amper} \cdot \frac{investmint\_period}{base\_investmint\_period\_amper} \cdot mint\_rate\_amper}\rfloor"></p>

## Volt minting

Volt mints by the following formula:

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}{volt} = \lfloor{\frac{hydrogent}{base\_investmint\_amount\_volt} \cdot \frac{investmint\_period}{base\_investmint\_period\_volt} \cdot mint\_rate\_volt}\rfloor"></p>

## Mint Rate (Amperes)

Mint rate is multiple coefficient for minting Amper tokens

It is halving every `base_halving_period_amper`

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}{mint\_rate\_amper_t} = \frac{mint\_rate\_amper\_init}{2^{\lfloor{\frac{t-1}{base\_halving\_period\_amper}}\rfloor}}"></p>


## Mint Rate (Voltes)

Mint rate is multiple coefficient for minting Volt tokens

It is halving every `base_halving_period_volt`

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}{mint\_rate\_volt_t} = \frac{mint\_rate\_volt\_init}{2^{\lfloor{\frac{t-1}{base\_halving\_period\_volt}}\rfloor}}"></p>


## Supply

Supply is the sum of liquid, vested and frozen tokens in each timestep.

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}boot\_supply_t = iquid\_boot_t %2B vested\_boot_t_u %2B frozen\_boot_t"></p>


## Assumptions

1. All agents lock tokens for the maximum available period defined in params for simulating
2. All agents mint maximum __**A**__ and __**V**__ tokens in 50/50 ratio

## Mathematical Specification

### Differential Equations

- liquid_boot - liquid network token
- vested_boot - locked(vested) network token (hydrogen)
- frozen_boot - not claimed(frozen) network token
- boot_inflation_rate_change - inflation rate change per timesep
- boot_supply - total network tokens supply
- inflation_rate_change_param - inflation per timestep in network tokens
- provision - timestep token provision
- amper - amper resource token
- volt - volt token
- mint_rate_amper
- mint_rate_volt
- cyberlinks - cyberlinks
- agents_count - the amount of the active agents
- capitalization_per_agent - the value of agent in ETH
- capitalization - network capitalization in ETH, cap is defined as `agent_count * capitalization_per_agent`

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}boot\_inflation\_rate_t = boot\_inflation\_rate_{t-1} %2B {\Delta boot\_inflation\_rate}"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}liquid\_boot_t = liquid\_boot_{t-1} %2B {\Delta liquid\_boot}"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}vested\_boot_t = vested\_boot_{t-1} %2B {\Delta vested\_boot}"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}frozen\_boot_t = frozen\_boot_{t-1} %2B {\Delta frozen\_boot}"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}amper_t = amper_{t-1} %2B {\Delta amper}"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}volt_t = volt_{t-1} %2B {\Delta volt}"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}cyberlinks_{t} = cyberlinks_{t-1} %2B {\Delta cyberlinks}"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}agents\_count_t = agents\_count_{t-1} %2B {\Delta agents\_count}"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}capitalization\_per\_agent_t = capitalization\_per\_agent_{t-1} %2B {\Delta capitalization\_per\_agent}"></p>


where the rate of change (<img src="https://render.githubusercontent.com/render/math?math=\color{green}\Delta">) is: 

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}\Delta boot\_inflation\_rate = \frac{\left(1 - \frac{vested\_ratio_{t-1}}{boot\_bonded\_share\_target}\right) \cdot boot\_inflation\_rate\_change\_annual}{timesteps\_per\_year}"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}{\Delta frozen\_boot} = 45404590000000 \cdot e^{-0.0648637x}"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}{\Delta vested\_boot} = \frac{liquid_{t-1}}{\frac{timesteps\_per\_year}{12} \cdot vesting\_speed} - {\Delta unvested\_boot}"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}{\Delta unvested\_boot} = \frac{vested\_boot_{t-1}}{\frac{timesteps\_per\_year}{12} \cdot unvesting\_speed}- {\Delta vested\_boot}"></p>
 
<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}{\Delta liquid\_boot} = - {\Delta frozen\_boot} - {\Delta vested\_boot} %2B timestep\_provision_{t-1} %2B {\Delta unvested\_boot}"></p>
 
<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}{\Delta amper} = \lfloor{\frac{\frac{1}{2} \cdot \Delta vested\_boot}{base\_investmint\_amount\_amper} \cdot \frac{investmint\_max\_period_t}{base\_investmint\_period\_amper} \cdot mint\_rate\_amper_{t}}\rfloor"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}{\Delta volt} = \lfloor{\frac{\frac{1}{2} \cdot \Delta vested\_boot}{base\_investmint\_amount\_volt} \cdot \frac{investmint\_max\_period_t}{base\_investmint\_period\_volt} \cdot mint\_rate\_volt_{t}}\rfloor"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}{\Delta agents\_count} = 18 \cdot t %2B 100"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}{\Delta cyberlinks} = \frac{6.3}{agents\_count^{0.3}} %2B extra\_links %2B guaranteed\_links" ></p> 

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}{\Delta capitalization\_per\_agent} = - \frac{start\_capitalization\_per\_agent \cdot agents\_count\_at\_activation^{0.7}}{agents\_count^{1.7}}"></p>

where:

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}{mint\_rate\_amper_t} = \frac{mint\_rate\_amper\_init}{2^{\lfloor{\frac{t-1}{base\_halving\_period\_amper}}\rfloor}}"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}{mint\_rate\_volt_t} = \frac{mint\_rate\_volt\_init}{2^{\lfloor{\frac{t-1}{base\_halving\_period\_volt}}\rfloor}}"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}timestep\_provision_{t-1} = \frac{boot\_supply_{t-1} \cdot boot\_inflation\_rate\_change_{t-1}}{timesteps\_per\_year}"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}vested\_ratio_{t-1} = \frac{vested\_boot}{boot\_supply}"></p>

<p style="text-align:center;"><img src="https://render.githubusercontent.com/render/math?math=\color{green}{investmint\_max\_period_t = investmint\_max\_period\_init \cdot 2^{\lfloor{\frac{t}{timesteps\_per\_year}}\rfloor}}"></p>  

## Summary of simulation parameters

- __*start_boot_supply*__ = `1e15`
- <img src="https://render.githubusercontent.com/render/math?math=\color{green}boot\_supply = start\_boot\_supply \cdot ( 1 %2B \frac{ 0.12}{1 %2B \frac{days}{365 \cdot 2}})^{\frac{days}{365}}">
- __*boot_inflation_rate_change*__  
- __*boot_inflation_max*__  
- __*boot_inflation_min*__  
- __*boot_bonded_share_target*__  
- __*agents_count_at_activation*__ `(10'000, 50'000, 100'000)`
- __*days_for_gift_activation*__ `(30, 100)`
- <img src="https://render.githubusercontent.com/render/math?math=\color{green}agents\_count = 9 \cdot days^2 %2B 100 \cdot days %2B agents\_count\_at\_activation">
- <img src="https://render.githubusercontent.com/render/math?math=\color{green}start\_capitalization\_per\_agent = 1">
- <img src="https://render.githubusercontent.com/render/math?math=\color{green}capitalization\_per\_agent = start\_capitalization\_per\_agent \cdot agents\_count\_at\_activation^{0.7} \cdot  agents\_count^{-0.7}">
- __*boot_bonded_share*__ `(0.7)`
- <img src="https://render.githubusercontent.com/render/math?math=\color{green}h\_supply = boot\_supply \cdot boot\_bonded\_share">
- __*extra_links*__ - function to define
- __*guaranteed_links*__ - function to define
- <img src="https://render.githubusercontent.com/render/math?math=\color{green}cyberlinks\_per\_agent = 9 \cdot agents\_count^{-0.3} %2B extra\_links %2B guaranteed\_links">
- __*investmint_period*__  
- __*investmint_amount*__  
- __*halving_time*__  
- __*investmint_max_period*__  
- __*a_v_ratio*__  

