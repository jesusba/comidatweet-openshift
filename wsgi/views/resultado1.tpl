<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <title>Resultados de la busqueda</title>
  </head>
  <body>
    <p><h3>ComidaTweet</h3></p>
    {% set contador = 0 %}
	{% for textop in textop %}
    <p><img alt="" class="app-icon" src="http://www.carat.co.uk/uploads/133597838026875/resize_then_crop_540_350.jpg" title="ComidaTweet" width="200" height="200"/></p>
    <h3>Resultado de la busqueda para {{ textop }}</h3>      
		<p>Contenido: {{ contenido[contador] }}</p>
		<p>Fecha: {{ fecha[contador] }}</p>
		<p>Autor: {{ autor[contador] }}</p>
		<p><img src="{{ avatar[contador] }}"/></p>
	{% set contador = contador + 1 %}
	{% endfor %}
    <form>
		<input type='button' value='VOLVER ATRAS' name='Back2' onclick='history.back()'/>
	</form>
  </body>
</html>
