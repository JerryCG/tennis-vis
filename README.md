# TennisVis
 * A project for visualizing tennis players statistics.
 * Published Python Dash App can be found at: https://tennis-vis.onrender.com or https://tennis-vis.herokuapp.com/ (maybe suspended)
 * Raw data source: https://tennisabstract.com, https://www.atptour.com/
 * Current Version: 2.4
 * Last data/ATP Rank update: 2025-04-14/2025-05-26
 * Current Functionality:
    1. [Home](https://tennis-vis.herokuapp.com/)
        - A Network for All ATP Grand Slam Champions in Tennis History
    2. [Dynamics](https://tennis-vis.herokuapp.com/dynamics)
        - ATP Dynamic Ranking from 2000-01-10 to 2025-05-26
        - GS Titles Accumulation of Important Players from 1990 to 2025
    3. [GeoTennis](https://tennis-vis.herokuapp.com/geotennis)
        - Geographic Distribution of ATP Top100 Players from 2000-01-10 to 2025-05-26
    4. [Records Search](https://tennis-vis.herokuapp.com/records)
        - A comprehensive match records search interface, criterions includes:
            - Dates
            - Opponents, e.g., Novak Djokovic, Top10 Players, Big3, Big4
            - Surfaces, e.g., Hard, Grass
            - Tournemants, e.g., Wimbledon, ATP1000, Olympics
            - Rounds, e.g., R128, QF, F
            - Results, e.g., win, tie-break lose
            - Streak, e.g., return the longest winning streak among matches of all previous seletions
            - Layout, e.g., lite or display all match statistics
    5. [Stats Visualization](https://tennis-vis.herokuapp.com/stats)
        - A graphic interface for multiple players stats comparison within a period:
            - Titles, e.g., all titles, grand slams
            - Head 2 Head, e.g., h2h on grass
            - Moveing Average Winning Ratio, e.g. MA winning ratio per 100 matches
            - Serve Stats, e.g., ace percent, second serve win percent
            - Points Overview, e.g., the distribution of Dominance Rate
            - Break Points Overview, e.g., average break points conversion rate
            - Win/Loss Counts, e.g., big heart matches vs crystal heart matches
            - Winning ratio by surface, e.g., on Clay
            - Winning ratio by tournament, e.g., finals of Australian Open
            - Winning ratio at rounds of Grand Slam, e.g., semi-finals on US Open
    6. [DSTennis](https://tennis-vis.herokuapp.com/ds)
        - A currently simple interface for visualizing regression results of tennis players' stats:
            - Variables are at the player level, e.g., height, weight, career winning ratio, career average dominant rate, left or right handed.
            - Simple linear regression displays the scatter plots and estimated regression line.
            - Multiple linear regression displays the estimated coefficients.