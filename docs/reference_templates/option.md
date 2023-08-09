### `{{ option.config_key }}` ### {: .purple .mb-0 }

`{{ option.comma_separated_display_args }}`
{: .purple .my-0 }

`{{ option.env_var }}`
{: .purple .mt-0}

{% if option.comma_separated_choices %}
one of: `{{ option.comma_separated_choices }}`
{: .green .pl-2 .mb-0 }
{% endif %}

default: `{{ option.default }}`
{: .green .pl-2 .my-0 }

{% if option.deprecated_message %}

{{ option.deprecated_message }}
{: .red .pl-2 .my-0 }

{{ option.removal_hint }}
{: .red .pl-2 .my-0 }

{% endif %}

{{ option.help|replace("\n", "<br>") }}
{: .pl-2 }

{% if option.target_field_name %}
{{ option.target_field_name }}
{% endif %}
