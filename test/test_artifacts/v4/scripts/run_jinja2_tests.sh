#!/bin/bash

set -e  

# Test 1: Basic template
python -c "
from jinja2 import Template
template = Template('Hello {{ name }}!')
result = template.render(name='John')
assert result == 'Hello John!', f'Expected \"Hello John!\", got \"{result}\"'
"

# Test 2: Conditional statements
python -c "
from jinja2 import Template
template = Template('{% if user %}Hello, {{ user }}!{% else %}Hello, stranger!{% endif %}')
result1 = template.render(user='Alice')
result2 = template.render(user=None)
assert result1 == 'Hello, Alice!', f'Expected \"Hello, Alice!\", got \"{result1}\"'
assert result2 == 'Hello, stranger!', f'Expected \"Hello, stranger!\", got \"{result2}\"'
"

# Test 3: Loops
python -c "
from jinja2 import Template
template = Template('{% for item in items %}{{ item }} {% endfor %}')
result = template.render(items=['apple', 'banana', 'cherry'])
assert result == 'apple banana cherry ', f'Expected \"apple banana cherry \", got \"{result}\"'
"

# Test 4: Filters
python -c "
from jinja2 import Template
template = Template('{{ name|upper }}')
result = template.render(name='john')
assert result == 'JOHN', f'Expected \"JOHN\", got \"{result}\"'
"

# Test 5: File system loader
echo "<h1>Hello, {{ name }}!</h1>" > /tmp/test_template.html
python -c "
from jinja2 import Environment, FileSystemLoader
import os
env = Environment(loader=FileSystemLoader('/tmp'))
template = env.get_template('test_template.html')
result = template.render(name='World')
assert result == '<h1>Hello, World!</h1>', f'Expected \"<h1>Hello, World!</h1>\", got \"{result}\"'
"
rm /tmp/test_template.html

python -c "
from jinja2 import Template, TemplateSyntaxError
try:
    Template('{% if %}')
    assert False, 'Should have raised TemplateSyntaxError'
except TemplateSyntaxError:
    print('Error handling test passed.')
"

# Test 7: Template inheritance
# base template
echo "{% block content %}Default content{% endblock %}" > /tmp/base.html
# child template
echo "{% extends 'base.html' %}{% block content %}Child content{% endblock %}" > /tmp/child.html

python -c "
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('/tmp'))
template = env.get_template('child.html')
result = template.render()
assert result == 'Child content', f'Expected \"Child content\", got \"{result}\"'
"

rm /tmp/base.html /tmp/child.html
