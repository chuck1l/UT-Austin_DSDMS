USE hr;

-- 1. Which region has the most operations?
SELECT
    r.region_name,
    COUNT(department_id) number_of_operations
FROM
	regions r
JOIN countries USING(region_id)
JOIN locations USING(country_id)
JOIN departments USING(location_id)
GROUP BY 1
ORDER BY 2 DESC
LIMIT 1;

-- 2. Which department has the most employees?
SELECT
	department_id,
    department_name,
    COUNT(employee_id) as number_of_employees
FROM departments
JOIN employees USING(department_id)
GROUP BY 1,2
ORDER BY 3 DESC
LIMIT 1;

-- 3. Which location has the most Departments?
SELECT
	l.location_id,
    l.city,
    COUNT(d.department_id) number_of_departments
FROM locations l
JOIN departments d
USING(location_id)
GROUP BY 1,2
ORDER BY 3 DESC
LIMIT 1;

-- 4. Which employee(s) is/are the latest hires??
SELECT e.employee_id, e.first_name, e.last_name, e.hire_date 
FROM employees e 
WHERE hire_date = (SELECT MAX(hire_date) FROM employees) ;

-- 5. Which region has a more operational cost?
SELECT
	r.region_id,
    r.region_name,
    SUM(salary) as operational_cost
FROM regions r
JOIN countries USING(region_id)
JOIN locations USING(country_id)
JOIN departments USING(location_id)
JOIN employees USING(department_id)
GROUP BY 1
LIMIT 1;

-- 6.	 How many employees have received the commission?
SELECT 
	COUNT(employee_id) number_of_employees
FROM employees 
WHERE commission_pct IS NOT NULL;

-- 7. Which departments don't have managers?
SELECT 
	department_id, 
	department_name 
FROM departments 
WHERE manager_id IS NULL;

-- 8. Who is the employee, not assigned to any department?
SELECT
	employee_id,
    CONCAT(first_name, " ", last_name) fullname
FROM employees 
WHERE department_id IS NULL;

-- 9. Which department has highest average salary?
SELECT
	emp.department_id,
    dept.department_name,
    AVG(emp.salary) AVERAGE_SALARY
FROM employees emp
JOIN departments dept USING(department_id)
WHERE department_id IS NOT NULL
GROUP BY 1
ORDER BY 3 DESC
LIMIT 1;

-- 10. Which city has more employees in Sales?
SELECT
	l.city,
	COUNT(e.employee_id) number_of_employees
FROM employees e
JOIN departments d USING(department_id)
JOIN locations l USING(location_id)
WHERE LOWER(d.department_name) IN ('sales') 
GROUP BY 1;    
 
