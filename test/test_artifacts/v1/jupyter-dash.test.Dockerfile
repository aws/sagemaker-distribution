ARG COSMOS_IMAGE
FROM $COSMOS_IMAGE

ARG MAMBA_DOCKERFILE_ACTIVATE=1

CMD ["python", "-c", "import plotly.express as px; import sys; fig = px.bar(x=['a', 'b', 'c'], y=[1, 3, 2]); fig.write_html('first_figure.html', auto_open=False)"]
