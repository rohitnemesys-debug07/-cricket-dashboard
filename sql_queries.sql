-- 1. Players from India
SELECT name, role
FROM players
WHERE team = 'India';

-- 2. Recent matches
SELECT team1, team2, status
FROM matches
ORDER BY id DESC
LIMIT 10;

-- 3. Top 10 run scorers
SELECT name, runs
FROM players
ORDER BY runs DESC
LIMIT 10;

-- 4. Players with high runs (>5000)
SELECT name, team, runs
FROM players
WHERE runs > 5000
ORDER BY runs DESC;

-- 5. Matches played by each team
SELECT team, COUNT(*) AS matches
FROM (
    SELECT team1 AS team FROM matches
    UNION ALL
    SELECT team2 FROM matches
) t
GROUP BY team
ORDER BY matches DESC;

-- 6. Count players by role
SELECT role, COUNT(*) AS total
FROM players
GROUP BY role;

-- 7. Highest runs
SELECT MAX(runs) AS highest_runs
FROM players;

-- 8. View all matches
SELECT * FROM matches;

 --9. All-rounders with good performance
SELECT name, runs, wickets
FROM players
WHERE role = 'All-rounder' AND runs > 1000 AND wickets > 50;

-- 10. Last 5 matches
SELECT team1, team2, status
FROM matches
ORDER BY id DESC
LIMIT 5;

-- 11. Player ranking by runs
SELECT name, runs
FROM players
ORDER BY runs DESC;

-- 12. Team performance (runs + wickets)
SELECT team,
       SUM(runs) AS total_runs,
       SUM(wickets) AS total_wickets
FROM players
GROUP BY team;

-- 13. Players scoring above 100
SELECT name, runs
FROM players
WHERE runs > 100;

-- 14. Top bowlers
SELECT name, wickets
FROM players
WHERE wickets > 50
ORDER BY wickets DESC;

-- 15. Medium performance players
SELECT name, runs
FROM players
WHERE runs BETWEEN 50 AND 100;

-- 16. Average runs per team
SELECT team, AVG(runs) AS avg_runs
FROM players
GROUP BY team;


-- 17. Total matches count
SELECT COUNT(*) AS total_matches
FROM matches;

-- 18. Top 5 wicket takers
SELECT name, wickets
FROM players
ORDER BY wickets DESC
LIMIT 5;

-- 19. Consistent players (avg runs)
SELECT name, AVG(runs) AS avg_runs
FROM players
GROUP BY name
ORDER BY avg_runs DESC;

-- 20. Player count per team
SELECT team, COUNT(*) AS players
FROM players
GROUP BY team;

-- 21. 🏆 Performance ranking (IMPORTANT)
SELECT name,
       (runs * 0.01 + wickets * 2) AS performance_score
FROM players
ORDER BY performance_score DESC;

-- 22. Head-to-head matches
SELECT team1, team2, COUNT(*) AS matches
FROM matches
GROUP BY team1, team2;

-- 23. Recently added players
SELECT name, runs
FROM players
ORDER BY id DESC
LIMIT 5;

-- 24. Players per team
SELECT team, COUNT(*) AS players_count
FROM players
GROUP BY team;

-- 25. Team performance trends
SELECT team,
       AVG(runs) AS avg_runs,
       AVG(wickets) AS avg_wickets
FROM players
GROUP BY team;