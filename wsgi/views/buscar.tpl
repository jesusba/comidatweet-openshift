<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <title>.::Usando la API de twitter::.</title>
  </head>
  <body>
    <p>Introduzca el nombre de un restaurante:</p>
    <br/>
    <form action="/buscar" method="post">
      <input type="text" name="nombre" id="name" placeholder="Introduzca aqui el nombre" class="cform-text" size="25"/>
      <p><input type="submit" class="button" value="Enviar" /></p>
    </form>
    <form action="/buscar" method="post">
      <input type="text" name="nombre1" id="name1" placeholder="Introduzca aqui el nombre con su ubicación" class="cform-text" size="25"/>
      <p><input type="submit" class="button" value="Enviar" /></p>
  </body>
</html>
