{% macro project_root() %}
  {{ modules.os.path.abspath(modules.os.path.join(project.project_root, '..')) | replace('\\', '/') }}
{% endmacro %}
