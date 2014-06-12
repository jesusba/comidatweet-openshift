<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <title>Resultados de la busqueda</title>
  </head>
  <body>
    <p><h3>ComidaTweet</h3></p>
    <p><img alt="" class="app-icon" src="http://www.carat.co.uk/uploads/133597838026875/resize_then_crop_540_350.jpg" title="ComidaTweet" width="200" height="200"/></p>
    <h3>Resultado de la busqueda</h3>      
    <p>
		<br>Palabra buscada: {{ palabra }}</br>
		<br>Contenido: {{ contenido }}</br>
		<br>Fecha: {{ fecha }}</br>
		<br>Autor: {{ autor }}</br>
	</p>
    <p><img src="{{ avatar }}"/></p>
    <form>
		<input type='button' value='VOLVER ATRAS' name='Back2' onclick='history.back()'/>
	</form>
  </body>
</html>
