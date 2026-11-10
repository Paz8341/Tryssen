# Tryssen

Web comunitaria estática en sueco e inglés, preparada para GitHub Pages y Pages CMS. Sin servidor propio, base de datos ni dependencias JavaScript. Los archivos de contenido son JSON y se editan con formularios visuales.

## Estado real de esta entrega

**Todavía no está publicada.** No se encontró un repositorio Tryssen accesible. Las imágenes del mensaje se pueden ver como referencia, pero no llegaron como archivos al entorno: falta incorporar el archivo original de la fotografía. El campo de portada está vacío deliberadamente; no se ha sustituido por otra fotografía. Se ha reproducido la estructura del boceto con CSS y SVG, pero no se ha verificado la fidelidad en un navegador. No hay noticias, eventos o álbumes inventados.

El proceso de publicación está configurado para detenerse hasta que se indiquen la fotografía principal, la persona responsable y el correo de contacto. La política de privacidad es un texto inicial que la responsable debe revisar para su caso real.

## Primera publicación: una sola vez

### Publicar el estado actual para revisar el diseño

Si quieres revisar la web antes de completar la portada y los datos de contacto, el workflow admite una ejecución manual: **Actions → Publicar Tryssen → Run workflow → revision: activado**. Esta opción omite únicamente los requisitos de portada, responsable y correo; mantiene las pruebas, la validación de contenidos y la optimización de imágenes. La web resultante será pública en GitHub Pages. Requiere autorización de la propietaria antes de publicar. Los commits automáticos y las ejecuciones manuales sin esta opción mantienen la comprobación estricta de la versión completa. No modifica el diseño ni añade contenido.

### Configuración del repositorio

1. En tu propia cuenta de GitHub crea un repositorio **público** llamado `tryssen`, con rama principal `main`. No añadas colaboradores, equipos con escritura, deploy keys de terceros ni otras aplicaciones con permisos de escritura. El repositorio público permite usar Pages en GitHub Free, dentro de sus límites.
2. Sube todo este proyecto a la raíz del repositorio. Deben quedar incluidos `.pages.yml` y `.github/workflows/pages.yml`. La subida por arrastrar carpetas en GitHub puede omitir carpetas ocultas; comprueba expresamente que están los dos archivos. Para importar todo de una vez, una persona que te ayude puede usar `git init`, `git add .`, `git commit` y `git push` al repositorio que acabas de crear.
3. En GitHub abre **Settings → Pages → Build and deployment → Source: GitHub Actions**.
4. Entra en **https://app.pagescms.org/** con tu cuenta de GitHub. Autoriza la aplicación oficial Pages CMS **solo para el repositorio tryssen**. Selecciona ese repositorio y la rama `main`. No invites colaboradores del CMS ni habilites editores adicionales.
5. En **Inställningar**, sube la **primera imagen original**, escribe el nombre de la persona responsable y el correo para pedir la retirada de fotos. Guarda. No uses la segunda imagen como fotografía: es el boceto de referencia.
6. En GitHub abre **Actions → Publicar Tryssen**. Espera a que los dos trabajos terminen en verde. La dirección se mostrará en **Settings → Pages**: normalmente `https://TU-USUARIO.github.io/tryssen/`.
7. Visita esa dirección y verifica las tareas de la lista al final. El editor permanecerá en una dirección externa; no existe una falsa pantalla `/admin`.

Si ya tienes un repositorio anterior, importa estos cambios allí después de guardar una copia. No crees una segunda web innecesariamente. Esta entrega no pudo inspeccionar un proyecto anterior porque no estaba disponible.

## Trabajo cotidiano sin código

Entra en https://app.pagescms.org/ y selecciona `tryssen`, rama `main`.

### Publicar una noticia

Abre **Nyheter**, añade un elemento en la lista, rellena **Titel (svenska)**, **Datum** y **Text (svenska)**. Los campos ingleses son opcionales. Puedes subir una imagen; en ese caso escribe **Bildbeskrivning (svenska)** para describirla. Activa **Publicerad** y guarda. Las noticias aparecen de más reciente a más antigua.

### Crear o cancelar una actividad

Abre **Aktiviteter**, añade un elemento e indica título, fecha y descripción en sueco. Hora opcional en formato `14:30`, hora local de Suecia; lugar y traducciones son opcionales. Activa **Publicerad** y guarda. Para cancelar, activa **Inställd** y guarda; se conserva la actividad con aviso. Para eliminar, borra el elemento y guarda. Las próximas se ordenan por fecha y hora; las anteriores se consultan desplegando **Tidigare aktiviteter**.

### Crear un álbum y subir varias fotos

En **Bildgalleri**, añade un elemento con título, descripción y fecha. En **Fotografier**, añade un elemento por imagen, sube el archivo y describe su contenido en sueco. Puedes cargar archivos previamente en **Media**, incluidos varios si el selector de tu navegador lo permite, y luego seleccionarlos desde cada elemento del álbum. El álbum admite tantas entradas como resulte razonable para los límites del alojamiento. En **Omslagsbild**, selecciona una de las imágenes incluidas en el álbum. Esa imagen aparece primero. Activa **Publicerad** y guarda.

Para añadir fotos después, abre el álbum y añade más elementos. Para quitar una foto, elimina su elemento y, si era la portada, elige otra. Guarda. Para borrar un álbum, elimina su elemento completo. Quitar una imagen del álbum no elimina el archivo del repositorio; borra también el archivo desde **Media** si ninguna publicación lo utiliza. Las imágenes se amplían mediante un botón: el visor admite Escape, flechas y navegación por teclado.

### Editar y borrar

Abre la sección, despliega el elemento, cambia los campos y guarda. Para ocultarlo, desactiva **Publicerad**. No guardes borradores sensibles: en un repositorio público también se pueden leer los archivos fuente y su historial. La web publicada excluye los borradores, pero GitHub no los vuelve privados.

### Idiomas

La primera visita abre en sueco. **SV | EN** cambia la interfaz y recuerda la preferencia en ese navegador. Los campos ingleses vacíos muestran el texto sueco original; no se traducen automáticamente. Fecha y hora se interpretan según Suecia. El contenido sueco conserva `lang="sv"` cuando se muestra en la interfaz inglesa.

## Cómo se actualiza automáticamente

Guardar en Pages CMS crea un commit en GitHub. Cada cambio en `main` ejecuta el workflow. Este comprueba los datos, prepara solo el contenido publicado, optimiza las fotos y publica `dist/`. No hace falta abrir Codex ni ejecutar comandos después de la configuración inicial. Si un trabajo falla, permanece la última versión publicada correctamente.

Todas las rutas del sitio son relativas: funcionan tanto en `/tryssen/` como en la raíz. El CMS escribe `/media/...`; el generador las convierte a rutas relativas y optimizadas. No publiques directamente la raíz del repositorio: el workflow publica únicamente `dist/`.

## Fotos y límites gratuitos

El build genera WebP de hasta 2400 × 1600, miniaturas de hasta 640 × 480, sin ampliar los originales. Elimina metadatos al recodificar. Solo publica las fotos referenciadas por contenido publicado. Los originales siguen en GitHub: reducir el peso del sitio no reduce automáticamente el historial del repositorio.

GitHub Pages tiene un límite de sitio publicado de 1 GB, un límite blando de transferencia de 100 GB/mes y límites de compilación y uso; consulta los vigentes en https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits. Evita fotos originales de varios megabytes: redimensiónalas antes de subir, usa JPG/WebP y conserva los originales de cámara fuera del repositorio. No subas vídeos grandes. GitHub bloquea archivos individuales de más de 100 MiB; no te acerques a ese límite.

Esta solución usa las modalidades gratuitas disponibles de GitHub Pages y el servicio alojado Pages CMS. No requiere compras ni suscripciones obligatorias para el uso comunitario previsto. Las condiciones de servicios externos pueden cambiar; no se puede garantizar su gratuidad indefinida. Los datos y el código permanecen en tu repositorio y el sitio ya publicado sigue funcionando sin Pages CMS. No actives productos de pago o ampliaciones de gasto.

## Privacidad y permisos

Completa el nombre y correo en **Inställningar** y revisa el texto de **Integritet & fotografier** antes de publicar. Comprueba base jurídica, consentimiento cuando corresponda, contexto identificable y derechos de imagen. No subas información sensible. Las fotos son públicas y se pueden copiar. Para solicitudes de retirada, elimina referencias y archivos; si hay datos sensibles en el historial, consulta el procedimiento de GitHub para eliminar datos sensibles y las cachés. Quitar un enlace no garantiza borrar todas las copias.

El sitio no contiene APIs de escritura, registro, comentarios ni contraseñas. La única escritura se realiza a través de GitHub y Pages CMS. Activa la autenticación de dos factores de GitHub. Revisa **Settings → Collaborators** y las aplicaciones instaladas: solo tu cuenta debe tener edición humana. Pages CMS y GitHub Actions necesitan permisos limitados para realizar su tarea. No incluyas tokens ni contraseñas en archivos. La exclusividad de permisos debe comprobarse en tu cuenta real; no ha podido verificarse en esta entrega.

## Problemas frecuentes

- **No veo cambios:** comprueba que guardaste en `main`, que **Publicerad** está activo y que Actions terminó en verde. Recarga la página.
- **Falla la primera publicación:** completa fotografía, responsable y correo en Inställningar; comprueba que Pages usa GitHub Actions.
- **Falla una foto:** usa JPG, PNG o WebP; no HEIC. No borres archivos utilizados. Añade descripción alternativa. La portada del álbum debe estar también en su lista de fotos.
- **Falla una fecha:** usa una fecha real. Hora en formato `HH:MM`.
- **No aparece el editor:** comprueba la instalación de la aplicación Pages CMS en el repositorio y que existe `.pages.yml` en `main`.
- **Se agotó una cuota:** reduce el volumen de imágenes y consulta Usage y la documentación de GitHub antes de activar cualquier pago.

## Recuperar una versión

En GitHub puedes abrir el historial del archivo de contenido y consultar versiones anteriores. Una persona que te ayude puede revertir el commit erróneo con `git revert`; el nuevo commit volverá a publicar automáticamente. Volver a ejecutar un workflow antiguo no restaura por sí solo el contenido de `main`. No compartas tu contraseña para pedir ayuda. Guarda copias periódicas del repositorio mediante **Code → Download ZIP**, especialmente antes de cambios grandes.

## Detener o eliminar la web

Para detenerla abre **Settings → Pages → Unpublish site**. Desactiva además el workflow en **Actions → Publicar Tryssen → … → Disable workflow**, para impedir que nuevos commits vuelvan a publicarla. Puedes desinstalar Pages CMS desde las aplicaciones instaladas de GitHub. Para eliminar todo, descarga antes una copia y borra el repositorio desde **Settings → General → Danger Zone**. Las copias y cachés externas no desaparecen necesariamente al borrar el repositorio.

## Verificación de esta entrega y tareas pendientes

Se incluyen pruebas reproducibles del generador: noticias publicadas/borradores, actividades canceladas, álbum con varias imágenes, rutas bajo un prefijo, fechas inválidas, imágenes fuera del repositorio y condiciones previas de publicación. También se valida la sintaxis JavaScript.

Pendiente por falta de archivos, repositorio y sesión de propietaria:

- Incorporar y comprobar que se usa exactamente la fotografía original.
- Comparar visualmente con el boceto en móvil, tablet y escritorio; verificar que no haya desbordamientos.
- Probar cuatro secciones, selector de idioma, persistencia, textos sin traducción, menú móvil y visor con teclado/lector de pantalla.
- Revisar contraste, foco y demás requisitos WCAG 2.2 AA; la implementación incluye ayudas, pero no constituye una auditoría de conformidad.
- Conectar Pages CMS, crear/publicar una noticia y actividad de prueba y un álbum de varias fotos, comprobar su aparición y luego eliminarlos.
- Comprobar que los commits disparan Actions, que todos los enlaces y fotos funcionan en `/tryssen/` y que una sesión de visitante no puede editar.
- Revisar permisos reales de GitHub, ausencia de secretos e información de privacidad.

## Para mantenimiento técnico

Python 3.12 y Node sirven para comprobar localmente, sin instalar paquetes JavaScript:

```sh
python -m unittest discover -s scripts -p 'test_*.py'
node --check assets/app.js
python scripts/build.py
```

El build básico copia fotos sin optimizar. El workflow instala Pillow 12.0.0 y usa `python scripts/build.py --optimize --strict`. Solo `dist/` es publicable. No hay servidor de aplicación. Mantén actualizados los Actions y Pillow mediante revisiones periódicas; conserva copias antes de actualizar.
