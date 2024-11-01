## Задание

![image](https://github.com/user-attachments/assets/1ee3197e-1df3-4617-8432-51149393d062)

### Решение находится в файле Task1_1.py

![image](https://github.com/user-attachments/assets/4cc9e006-1e3f-4b66-8165-32b53beedf54)

### Решение находится в директории Task1_2

# Запуск 
    git clone https://github.com/EgorZhizhlo/MillionAgentsTask.git
    cd MillionAgentsTask
    docker build -t converter .
    docker run -d -p 8000:8000/tcp converter

## Сайт будет доступен по адрессу http://localhost:8000

![image](https://github.com/user-attachments/assets/91da27ef-35a9-41fb-90cb-5b8b88124850)

### Решение:
    SELECT 
        user_id,
        SUM(CASE WHEN EXTRACT(YEAR FROM created_at) = 2022 THEN reward ELSE 0 END) AS reward_sum_2022
    FROM 
        reports
    GROUP BY 
        user_id
    HAVING 
        MIN(EXTRACT(YEAR FROM created_at)) = 2021;

![image](https://github.com/user-attachments/assets/b063493b-5c15-4588-affa-a02dce4a76bd)

### Решение:
    SELECT 
        r.barcode,
        r.price
    FROM 
        reports r
    JOIN 
        pos p ON r.pos_id = p.id
    GROUP BY 
        r.barcode, r.price
    HAVING 
        COUNT(DISTINCT p.title) > 1;
