-- Custom test to validate if review score is b/w 1.0 and 10.0

{% test validate_review_score(model, column_name) %}
SELECT *
FROM {{ model }}
WHERE {{ column_name }} NOT BETWEEN 1.0 AND 10.0
{% endtest %}

