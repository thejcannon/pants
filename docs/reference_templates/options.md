# {{ scope | default("Global options", true) }}

---

{% if is_goal%}

```
pants {{ scope }} [args]
```

{% endif %}
{{ description }}

Backend: <span style="color: purple"><code>{{ provider }}</code></span>
<br>
Config section: <span style="color: purple"><code>[{{ scope | default("GLOBAL", true) }}]</code></span>

## Basic options

{% for option in basic %}

    {%- include 'option.md' %}

{% else %}

    None

{% endfor %}

## Advanced options

{% for option in advanced %}

    {%- include 'option.md' %}

{% else %}

    None

{% endfor %}

## Deprecated options

{% for option in deprecated %}

    {%- include 'option.md' %}

{% else %}

    None

{% endfor %}

{% if related_subsystem %}

## Related subsystems

    {% for option in comma_separated_consumed_scopes %}
        {% include 'option.md' %}
    {% endfor %}

{% endif %}
