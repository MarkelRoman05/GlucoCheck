# Fase 1 — Documentación y Diseño Técnico

## Índice

1. Título del proyecto e integrantes
   - 1.1 Título del proyecto
   - 1.2 Descripción breve
   - 1.3 Equipo de desarrollo
   - 1.4 Contexto académico

2. Resumen ejecutivo

3. Descripción funcional del sistema
   - 3.1 Perfil del usuario
   - 3.2 Flujo de uso del sistema
   - 3.3 Datos de entrada
   - 3.4 Resultado obtenido
   - 3.5 Advertencia sobre el alcance del sistema
   - 3.6 Limitaciones del sistema

4. Alcance definitivo (IN / OUT)
   - 4.1 Dentro del alcance (IN)
   - 4.2 Fuera del alcance (OUT)

5. Arquitectura del sistema
   - 5.1 Justificación del enfoque de modelado

6. Tecnologías seleccionadas
   - 6.1 Capa de datos
   - 6.2 Capa de modelado
   - 6.3 Capa de presentación
   - 6.4 Infraestructura y reproducibilidad
   - 6.5 Consideraciones de diseño arquitectónico

7. Modelo de datos
   - 7.1 Estructura general del conjunto de datos
   - 7.2 Variable objetivo
   - 7.3 Variables predictoras
   - 7.4 Preprocesamiento
   - 7.5 Restricciones del modelo de datos

8. Datos
   - 8.1 Origen y naturaleza del conjunto de datos
   - 8.2 Finalidad del uso de los datos
   - 8.3 Reproducibilidad y transparencia

9. Ética, legalidad y accesibilidad
   - 9.1 Consideraciones éticas
   - 9.2 Cumplimiento legal
   - 9.3 Accesibilidad y uso responsable

10. Backlog inicial
    - 10.1 Funcionalidades núcleo (alta prioridad)
    - 10.2 Funcionalidades complementarias (prioridad media)
    - 10.3 Mejoras evolutivas (prioridad baja)

11. Plan de trabajo
    - 11.1 Fase 1 – Preparación y análisis del conjunto de datos
    - 11.2 Fase 2 – Desarrollo y validación del modelo
    - 11.3 Fase 3 – Integración y desarrollo de la interfaz
    - 11.4 Fase 4 – Pruebas finales y documentación

12. Estrategia de desarrollo
    - 12.1 Modelo de ciclo de vida
    - 12.2 Gestión de versiones y control de cambios
    - 12.3 Integración progresiva de componentes
    - 12.4 Trazabilidad y coherencia metodológica
    - 12.5 Validación y control del modelo

13. Riesgos técnicos actualizados
    - 13.1 Riesgo de sobreajuste del modelo
    - 13.2 Riesgo de dependencia del conjunto de datos
    - 13.3 Riesgo de deriva del modelo
    - 13.4 Riesgo de interpretabilidad limitada
    - 13.5 Riesgo de integración entre componentes

14. Repositorio del proyecto

---

## 1. Título del proyecto e integrantes

### 1.1 Título del proyecto

**GlucoCheck: Sistema de Clasificación del Riesgo de Diabetes Tipo 2 mediante Técnicas de Big Data e Inteligencia Artificial**

### 1.2 Descripción breve

GlucoCheck es un proyecto académico enmarcado en el ámbito del Big Data y la Inteligencia Artificial, cuyo objetivo es diseñar y desarrollar un sistema capaz de clasificar el nivel de riesgo de diabetes tipo 2 en individuos a partir de variables clínicas y biométricas. El sistema integra un pipeline de procesamiento de datos, modelos de aprendizaje automático supervisado y una capa de visualización interactiva orientada a la exploración analítica de los resultados.

El proyecto responde a una necesidad real del sector sanitario: la identificación temprana de perfiles de riesgo asociados a la diabetes tipo 2, una enfermedad crónica de alta prevalencia a nivel mundial. GlucoCheck no sustituye el diagnóstico médico ni realiza monitorización continua de pacientes; su alcance se limita a la clasificación del riesgo a partir de datos estáticos, proporcionando una herramienta de apoyo a la toma de decisiones basada en evidencia analítica.

### 1.3 Equipo de desarrollo

El equipo está compuesto por cuatro integrantes, cada uno con un rol especializado que cubre las áreas técnicas clave del proyecto:

| Integrante | Rol | Responsabilidades principales |
|---|---|---|
| **Markel** | Data Engineer | Diseño e implementación del pipeline de datos, ingesta, transformación (ETL/ELT) y gestión del almacenamiento en el Data Lake / Data Warehouse. |
| **Steven** | ML Engineer | Selección, entrenamiento, evaluación y despliegue de los modelos de Machine Learning para la predicción del riesgo de diabetes. |
| **Juan Carlos** | DevOps | Configuración de la infraestructura, gestión de contenedores, integración y despliegue continuo (CI/CD) y monitorización técnica y mantenimiento de la infraestructura. |
| **Miguel Ángel** | Frontend / BI | Desarrollo de la interfaz de usuario, diseño de dashboards interactivos y visualización de los resultados analíticos mediante herramientas de BI. |

### 1.4 Contexto académico

Este proyecto se desarrolla como parte del módulo de Proyecto del programa de **Big Data e Inteligencia Artificial**, con el objetivo de aplicar de forma integrada las competencias adquiridas a lo largo del programa en un caso de uso real y socialmente relevante.

---

## 2. Resumen ejecutivo

La diabetes tipo 2 representa uno de los mayores desafíos de salud pública a nivel global. Según la Organización Mundial de la Salud, más de 422 millones de personas padecen esta enfermedad, y su prevalencia continúa en aumento vinculada a factores como el sedentarismo, la obesidad y el envejecimiento poblacional. Uno de los principales problemas asociados a esta patología es su diagnóstico tardío: en muchos casos, los individuos acumulan años de exposición a niveles elevados de glucosa antes de recibir un diagnóstico formal, lo que incrementa significativamente el riesgo de complicaciones crónicas como enfermedades cardiovasculares, neuropatía o insuficiencia renal.

GlucoCheck propone abordar esta problemática mediante el desarrollo de un sistema de clasificación del riesgo de diabetes tipo 2 basado en técnicas de Big Data e Inteligencia Artificial. A partir de variables clínicas y biométricas de carácter estático —como niveles de glucosa en ayunas, índice de masa corporal, presión arterial o historial familiar—, el sistema aplica modelos de aprendizaje automático supervisado para clasificar a un individuo en distintos niveles de riesgo. El resultado se presenta a través de una interfaz web que permite consultar y explorar los resultados de forma clara e intuitiva.

Es importante destacar que el alcance del sistema es deliberadamente acotado: GlucoCheck no realiza monitorización continua de pacientes, no accede a datos clínicos en tiempo real y no emite diagnósticos médicos. Su función es la de una herramienta de apoyo orientada a la identificación de perfiles de riesgo, cuya interpretación debe realizarse siempre en el contexto de una valoración clínica profesional.

Desde el punto de vista técnico, el proyecto integra un pipeline de procesamiento de datos que abarca las etapas de ingesta, limpieza, transformación y almacenamiento, sobre el que se entrena y evalúa un modelo de clasificación supervisada. La infraestructura se gestiona mediante contenedores y se despliega siguiendo prácticas modernas de desarrollo y entrega de software. Los resultados analíticos se exponen a través de una capa de visualización interactiva orientada a la exploración y comunicación de los resultados del modelo.

El impacto esperado del proyecto es doble: por un lado, demostrar la viabilidad técnica de aplicar metodologías de Big Data e IA a un problema sanitario real; por otro, generar un artefacto funcional que sirva como base para futuras iteraciones o como referencia metodológica en entornos académicos y de investigación aplicada.

## 3. Descripción funcional del sistema

### 3.1 Perfil del usuario

GlucoCheck está orientado a dos perfiles de usuario principales. En primer lugar, profesionales del ámbito sanitario o de la salud pública que deseen explorar patrones de riesgo en conjuntos de datos clínicos con fines analíticos o de investigación. En segundo lugar, usuarios con formación técnica o científica —como estudiantes, investigadores o analistas de datos— interesados en aplicar modelos de clasificación sobre variables biométricas. En ningún caso el sistema está dirigido a pacientes sin formación adecuada para interpretar sus resultados, dado que no emite diagnósticos médicos ni recomendaciones terapéuticas.

### 3.2 Flujo de uso del sistema

El sistema sigue un flujo de interacción lineal y estructurado en las siguientes etapas:

1. **Acceso a la interfaz**: el usuario accede a la aplicación web a través de un navegador, sin necesidad de instalación local.
2. **Introducción de datos**: el usuario introduce manualmente un conjunto de variables clínicas y biométricas correspondientes a un individuo.
3. **Envío y procesamiento**: el sistema recibe los datos, los valida y los procesa aplicando el modelo de clasificación previamente entrenado.
4. **Visualización del resultado**: el sistema devuelve una clasificación del nivel de riesgo de diabetes tipo 2, acompañada de una representación visual del resultado.
5. **Consulta de información complementaria**: el usuario puede acceder a una vista analítica con información contextual sobre las variables introducidas y su peso relativo en la clasificación.

### 3.3 Datos de entrada

El sistema requiere la introducción de las siguientes variables para generar una clasificación:

- Nivel de glucosa en ayunas
- Índice de masa corporal (IMC)
- Presión arterial diastólica
- Grosor del pliegue cutáneo tricipital
- Nivel de insulina sérica
- Edad
- Número de embarazos (aplicable según perfil)
- Función de pedigrí de diabetes (antecedentes familiares)

Estas variables corresponden a las recogidas en el conjunto de datos de referencia utilizado para el entrenamiento del modelo, por lo que el sistema no admite, en su versión actual, variables adicionales no contempladas en dicho conjunto.

### 3.4 Resultado obtenido

El sistema devuelve una clasificación del nivel de riesgo de diabetes tipo 2 a partir de la probabilidad estimada por el modelo. Aplicando umbrales definidos sobre dicha probabilidad, el resultado se categoriza en uno de los tres niveles siguientes:

- **Riesgo bajo** *(verde)*: la probabilidad estimada se sitúa por debajo del umbral inferior. Las variables introducidas no presentan una combinación de indicadores estadísticamente relevante para la clasificación positiva.
- **Riesgo moderado** *(amarillo)*: la probabilidad estimada se sitúa entre los umbrales inferior y superior. Las variables introducidas presentan algunos indicadores asociados al riesgo, sin alcanzar el nivel de certeza estadística del nivel alto.
- **Riesgo alto** *(rojo)*: la probabilidad estimada supera el umbral superior. Las variables introducidas presentan una combinación de indicadores estadísticamente asociada a un perfil de riesgo elevado.

Los valores concretos de los umbrales se determinarán durante la fase de entrenamiento y evaluación del modelo, atendiendo a criterios de rendimiento como la sensibilidad y la especificidad. El resultado se acompaña de una representación visual y de los valores introducidos, sin que el sistema emita ningún tipo de recomendación clínica o terapéutica.

La definición definitiva de los umbrales se realizará durante la fase de validación del modelo, empleando métricas de evaluación estándar como la sensibilidad, la especificidad y el análisis de la curva ROC. Dado el contexto clínico del problema, se priorizará la minimización de falsos negativos en el nivel de riesgo alto, por cuanto una clasificación errónea en este estrato tiene mayor relevancia desde el punto de vista sanitario. La estrategia de umbralización buscará, en último término, un equilibrio entre la capacidad discriminativa del modelo y la utilidad interpretativa del resultado para el usuario.

### 3.5 Advertencia sobre el alcance del sistema

> **Aviso importante**: GlucoCheck es una herramienta de apoyo analítico con fines académicos. Los resultados obtenidos no constituyen un diagnóstico médico, no sustituyen la valoración de un profesional de la salud y no deben ser utilizados para tomar decisiones clínicas. Ante cualquier duda sobre el estado de salud, el usuario debe consultar a un médico.

### 3.6 Limitaciones del sistema

- El modelo ha sido entrenado sobre un conjunto de datos específico y puede no ser representativo de todas las poblaciones.
- El sistema no contempla variables contextuales como hábitos de vida, medicación activa o historial clínico completo.
- No realiza seguimiento longitudinal ni comparación entre consultas sucesivas.
- Los resultados pueden verse afectados por valores atípicos o datos incompletos introducidos por el usuario.
- La estabilidad y generalización de los umbrales definidos dependen de la calidad, tamaño y representatividad del conjunto de datos utilizado para el entrenamiento y validación del modelo. Cambios en la distribución poblacional o en el perfil clínico de los individuos podrían requerir una recalibración periódica del sistema para mantener su validez predictiva.

## 4. Alcance definitivo (IN / OUT)

El presente apartado delimita de forma explícita el alcance funcional del sistema GlucoCheck, distinguiendo entre aquello que el sistema contempla y lo que queda fuera de su ámbito de actuación.

### 4.1 Dentro del alcance (IN)

- Clasificación del nivel de riesgo de diabetes tipo 2 a partir de un conjunto de variables clínicas y biométricas previamente definidas y acotadas.
- Operación sobre datos estáticos introducidos manualmente por el usuario a través de la interfaz web, sin conexión a fuentes de datos externas.
- Estimación de la probabilidad de riesgo mediante un modelo de clasificación supervisada y su categorización en tres niveles: bajo, moderado y alto.
- Presentación del resultado al usuario mediante una interfaz web con representación visual interpretativa.

### 4.2 Fuera del alcance (OUT)

- El sistema **no realiza diagnóstico médico** de ningún tipo, ni en sentido clínico ni legal.
- El sistema **no sustituye la valoración profesional** de un médico u otro profesional sanitario habilitado.
- El sistema **no accede a historias clínicas reales** ni a datos provenientes de sistemas de información sanitaria o fuentes en tiempo real.
- El sistema **no realiza monitorización longitudinal** de pacientes ni permite el seguimiento temporal de un mismo individuo.
- El sistema **no admite variables adicionales** no contempladas en el conjunto de datos de entrenamiento, ni generaliza a perfiles clínicos fuera de dicho dominio.
- El sistema **no toma decisiones automatizadas** sobre tratamientos, intervenciones clínicas o derivaciones asistenciales.

## 5. Arquitectura del sistema

### 5.1 Justificación del enfoque de modelado

La elección del paradigma de aprendizaje supervisado para el componente de modelado de GlucoCheck responde a las características intrínsecas del problema y del conjunto de datos disponible. El dataset utilizado incluye una variable objetivo previamente etiquetada que indica la presencia o ausencia de diabetes tipo 2 en cada registro, lo que hace viable y metodológicamente adecuado el uso de algoritmos de clasificación supervisada. El objetivo del sistema no es descubrir agrupaciones o patrones latentes en los datos —tarea propia de los métodos no supervisados—, sino estimar la probabilidad de que un individuo pertenezca a una categoría de riesgo definida con antelación.

Una ventaja fundamental del enfoque supervisado en este contexto es la posibilidad de evaluar el rendimiento del modelo de forma objetiva, mediante métricas contrastadas como la sensibilidad, la especificidad, el área bajo la curva ROC u otras medidas de discriminación clínicamente interpretables. Esta capacidad de validación frente a una referencia conocida resulta esencial para justificar la utilidad del sistema como herramienta de apoyo analítico.

Los métodos no supervisados podrían tener un valor exploratorio en fases previas de análisis —por ejemplo, para identificar subgrupos poblacionales en los datos—, pero no permiten validar directamente la capacidad predictiva del sistema frente a una etiqueta clínica de referencia. Por este motivo, se descartan como enfoque principal del componente de clasificación, sin perjuicio de que puedan emplearse de forma auxiliar en etapas de análisis exploratorio de datos.

## 6. Tecnologías seleccionadas

La selección de tecnologías para GlucoCheck responde a criterios de adecuación al problema, madurez del ecosistema, reproducibilidad del entorno y coherencia con el alcance académico del proyecto. A continuación se describen las decisiones tecnológicas adoptadas, organizadas por capa funcional del sistema.

### 6.1 Capa de datos

Para el procesamiento, limpieza y transformación de los datos se empleará **Python** como lenguaje principal, dada su consolidada posición en el ámbito del análisis de datos y la computación científica. Python ofrece un ecosistema amplio de librerías especializadas para la manipulación de datos tabulares, el análisis estadístico exploratorio y la preparación de conjuntos de entrenamiento. Su uso en este proyecto se justifica tanto por su idoneidad técnica como por su adopción generalizada en entornos de investigación y ciencia de datos.

El conjunto de datos de referencia se almacenará en un formato estructurado compatible con las herramientas de procesamiento seleccionadas. No se contempla el uso de sistemas de gestión de bases de datos distribuidas ni de infraestructuras de procesamiento en tiempo real, en coherencia con el alcance estático del sistema.

### 6.2 Capa de modelado

El entrenamiento, evaluación y serialización del modelo de clasificación supervisada se realizará íntegramente en Python, haciendo uso de librerías estándar del ecosistema científico orientadas al aprendizaje automático. Estas librerías permiten la implementación de distintos algoritmos de clasificación, la evaluación mediante métricas de rendimiento y la exportación del modelo entrenado para su integración en la capa de presentación.

### 6.3 Capa de presentación

La interfaz de usuario se desarrollará como una aplicación web ligera que permita la introducción de variables y la visualización del resultado de clasificación. Se optará por un marco de desarrollo web de bajo peso, adecuado para prototipos funcionales de carácter académico, que facilite la integración con el modelo serializado sin requerir infraestructura compleja.

### 6.4 Infraestructura y reproducibilidad

Con el objetivo de garantizar la reproducibilidad del entorno de ejecución y facilitar el despliegue del sistema en distintas máquinas, se contempla la contenedorización de los componentes mediante tecnologías de virtualización ligera basadas en contenedores. Este enfoque permite aislar las dependencias del proyecto, asegurar la consistencia entre entornos de desarrollo y producción, y simplificar el proceso de puesta en marcha del sistema por parte de terceros.

### 6.5 Consideraciones de diseño arquitectónico

La arquitectura adoptada sigue un enfoque modular por capas, en el que cada componente tiene una responsabilidad bien delimitada. La separación entre la capa de modelado y la capa de presentación permite la sustitución o actualización futura del modelo sin necesidad de modificar la interfaz de usuario. Este desacoplamiento favorece la mantenibilidad del sistema, su escalabilidad en un contexto académico y la posibilidad de evolución incremental a lo largo del ciclo de vida del proyecto.

## 7. Modelo de datos

### 7.1 Estructura general del conjunto de datos

El conjunto de datos empleado en GlucoCheck presenta una estructura tabular en la que cada fila representa un individuo y cada columna corresponde a una variable clínica, biométrica o a la variable de resultado. Esta organización es propia de los problemas de clasificación supervisada y permite aplicar directamente los algoritmos de aprendizaje automático seleccionados sin transformaciones estructurales previas.

### 7.2 Variable objetivo

La variable objetivo es de naturaleza binaria e indica la presencia o ausencia de diabetes tipo 2 en el individuo registrado. Esta etiqueta constituye la referencia sobre la que el modelo se entrena y frente a la que se evalúa su capacidad de clasificación. Al tratarse de una variable supervisada, su calidad y fiabilidad son determinantes para el rendimiento y la validez del sistema.

### 7.3 Variables predictoras

Las variables predictoras del modelo se distribuyen en las siguientes categorías generales:

- **Variables biométricas continuas**: recogen mediciones fisiológicas cuantitativas del individuo, como niveles de glucosa, presión arterial, índice de masa corporal o concentración de insulina. Sus valores pueden variar de forma continua dentro de rangos clínicamente definidos.
- **Variables discretas o de conteo**: incluyen variables numéricas enteras que representan frecuencias o recuentos, como el número de embarazos previos.
- **Variables derivadas o compuestas**: recogen información calculada a partir de otros parámetros, como la función de pedigrí de diabetes, que sintetiza la influencia del historial familiar en una puntuación numérica.

### 7.4 Preprocesamiento

Antes de ser utilizadas en el entrenamiento o en la inferencia, las variables del sistema requieren un proceso de validación y transformación que incluye la detección y tratamiento de valores ausentes o atípicos, la normalización o estandarización de las variables continuas, y la verificación de que los valores introducidos se encuentran dentro de los rangos admisibles para el modelo. Este preprocesamiento es indispensable para garantizar la coherencia entre los datos de entrenamiento y los datos de entrada en producción.

### 7.5 Restricciones del modelo de datos

El sistema únicamente admite como entrada las variables presentes en el conjunto de datos de entrenamiento. No es posible incorporar variables adicionales no contempladas en dicho conjunto sin reentrenar el modelo, dado que cualquier modificación del espacio de características requeriría una revisión completa del pipeline de modelado.

Asimismo, el modelo de clasificación aprende relaciones estadísticas a partir del conjunto de datos de entrenamiento, sin establecer vínculos causales entre las variables clínicas y el resultado. Las asociaciones identificadas deben interpretarse como patrones predictivos derivados de los datos disponibles, y no como evidencia de causalidad clínica directa.

## 8. Datos

### 8.1 Origen y naturaleza del conjunto de datos

GlucoCheck utiliza un conjunto de datos público, anonimizado y ampliamente empleado en la comunidad científica para el desarrollo y evaluación de modelos de clasificación del riesgo de diabetes tipo 2. Este dataset ha sido utilizado de forma recurrente en investigación académica y en entornos de formación en ciencia de datos, lo que avala su idoneidad como referencia metodológica para el presente proyecto.

El conjunto de datos no contiene información de carácter personal ni ningún dato que permita la identificación directa o indirecta de los individuos registrados. Todos los registros están anonimizados y estructurados exclusivamente como observaciones numéricas de variables clínicas y biométricas, coherentes con el modelo de datos descrito en el apartado 7.

Dado su carácter público y anonimizado, el conjunto de datos empleado no está sujeto a tratamiento de datos personales en el marco del presente proyecto. En consecuencia, su utilización con fines académicos no implica obligaciones adicionales derivadas de la normativa de protección de datos personales.

### 8.2 Finalidad del uso de los datos

El uso del conjunto de datos se circunscribe estrictamente a fines académicos y de validación metodológica. No se realiza ningún tipo de tratamiento de datos personales reales, ni se establece integración con sistemas de información clínica, historias médicas electrónicas u otras fuentes de datos sanitarios. El proyecto no contempla la recolección, almacenamiento ni procesamiento de datos de individuos reales en ninguna de sus fases.

### 8.3 Reproducibilidad y transparencia

La elección de un conjunto de datos público favorece la reproducibilidad del proyecto, en tanto que cualquier investigador o evaluador puede acceder a los mismos datos y verificar de forma independiente los resultados obtenidos. Este principio de transparencia es coherente con los estándares de integridad metodológica propios del entorno académico y científico.

## 9. Ética, legalidad y accesibilidad

### 9.1 Consideraciones éticas

GlucoCheck se concibe como una herramienta de apoyo analítico con fines exclusivamente académicos, y su diseño incorpora desde la fase inicial una reflexión sobre las implicaciones éticas derivadas del uso de modelos predictivos en contextos con dimensión clínica. El sistema no sustituye en ningún caso el juicio de un profesional sanitario, y sus resultados no deben ser interpretados como orientación médica de ningún tipo.

Uno de los riesgos éticos identificados es la posibilidad de que los usuarios malinterpreten los niveles de riesgo devueltos por el sistema como diagnósticos definitivos. Para mitigar este riesgo, el sistema incorpora advertencias explícitas sobre el alcance y las limitaciones de los resultados, tal y como se recoge en el apartado 3.5. Asimismo, se considera esencial que el funcionamiento del modelo sea transparente en la medida de lo posible, de modo que el usuario comprenda que los resultados se derivan de relaciones estadísticas aprendidas a partir de datos históricos, y no de una evaluación clínica individualizada.

Asimismo, se reconoce que los modelos predictivos pueden verse afectados por sesgos derivados de la composición del conjunto de datos de entrenamiento. Diferencias demográficas o clínicas insuficientemente representadas podrían influir en el rendimiento del sistema en determinados subgrupos poblacionales. En consecuencia, cualquier aplicación futura en contextos reales requeriría procesos adicionales de validación externa, análisis de equidad y revisión periódica del desempeño del modelo para garantizar su uso responsable.

### 9.2 Cumplimiento legal

Desde el punto de vista legal, GlucoCheck no realiza tratamiento de datos personales reales en ninguna de sus fases. El conjunto de datos empleado es de carácter público y anonimizado, por lo que no contiene información que permita la identificación de individuos y su uso académico no genera obligaciones adicionales en materia de protección de datos, como ya se indicó en el apartado 8.1.

El sistema no toma decisiones automatizadas con efectos jurídicos, clínicos o administrativos sobre ninguna persona. Asimismo, GlucoCheck no se enmarca ni se presenta como un dispositivo médico, producto sanitario o herramienta de diagnóstico clínico y, en el marco del presente proyecto académico y conforme al alcance funcional definido, no está sujeto a los requisitos regulatorios aplicables a este tipo de sistemas.

### 9.3 Accesibilidad y uso responsable

El diseño de la interfaz de usuario priorizará la claridad interpretativa de los resultados, evitando visualizaciones ambiguas o representaciones que puedan inducir a conclusiones erróneas. Se aplicarán principios básicos de accesibilidad digital, entre los que se incluyen el uso de contraste adecuado entre elementos visuales, el empleo de un lenguaje claro y no técnico en los mensajes dirigidos al usuario, y la presentación de los resultados de clasificación de forma comprensible e inequívoca.

En línea con lo establecido en el apartado 3.1, el sistema no está orientado a pacientes sin formación sanitaria o técnica adecuada para interpretar sus resultados. El diseño responsable de la interfaz incluirá mecanismos que refuercen esta limitación, como avisos de uso y contextualizaciones del resultado que recuerden al usuario la necesidad de contrastar cualquier información con un profesional de la salud.

## 10. Backlog inicial

El backlog inicial del proyecto GlucoCheck recoge el conjunto estructurado de funcionalidades y tareas necesarias para desarrollar el sistema conforme al alcance definido en apartados anteriores. Los elementos se priorizan atendiendo a criterios de valor académico, coherencia técnica y dependencia funcional entre componentes.

### 10.1 Funcionalidades núcleo (alta prioridad)

- Implementación del pipeline de carga y preprocesamiento del conjunto de datos.
- Desarrollo del modelo de clasificación supervisada y su proceso de validación interna.
- Definición de los umbrales de categorización del riesgo conforme a criterios metodológicos.
- Serialización del modelo entrenado para su integración en la capa de presentación.
- Desarrollo de la interfaz web para introducción de variables y visualización del resultado.

Estas funcionalidades constituyen el núcleo mínimo viable del sistema y permiten demostrar la viabilidad técnica del proyecto.

### 10.2 Funcionalidades complementarias (prioridad media)

- Incorporación de visualizaciones explicativas del resultado.
- Mejora de la validación de entradas mediante controles adicionales.
- Documentación técnica detallada del pipeline de modelado.
- Implementación de mecanismos básicos de trazabilidad del proceso de inferencia.

Estas tareas refuerzan la robustez y claridad interpretativa del sistema, sin alterar su alcance funcional principal.

### 10.3 Mejoras evolutivas (prioridad baja)

- Evaluación comparativa de distintos algoritmos de clasificación supervisada.
- Análisis adicional de estabilidad del modelo ante distintas particiones del conjunto de datos.
- Optimización de la experiencia de usuario desde el punto de vista de accesibilidad.
- Preparación del sistema para futuras extensiones académicas.

Estas mejoras se contemplan como posibles extensiones del proyecto, subordinadas a la disponibilidad temporal y siempre dentro del marco académico definido.

La organización del backlog responde a un enfoque iterativo e incremental, que permite desarrollar el sistema por fases funcionales claramente delimitadas y facilita la validación progresiva de cada componente antes de su integración completa. Este planteamiento contribuye a reducir riesgos técnicos, mejorar la trazabilidad del desarrollo y asegurar la coherencia entre los objetivos académicos y la implementación efectiva del sistema.

## 11. Plan de trabajo

El plan de trabajo organiza el desarrollo del proyecto en fases secuenciales con validación incremental, en coherencia con el backlog inicial y la estrategia iterativa definida. Cada fase contempla objetivos concretos y resultados verificables antes de avanzar a la siguiente etapa.

### 11.1 Fase 1 – Preparación y análisis del conjunto de datos

En esta fase se realiza la revisión estructural del dataset seleccionado, la validación de su integridad y la preparación del entorno de trabajo. Se documentan las variables disponibles, su tipología y su coherencia con el modelo de datos definido. El resultado esperado es un conjunto de datos listo para el proceso de modelado.

### 11.2 Fase 2 – Desarrollo y validación del modelo

Se implementa el modelo de clasificación supervisada y se ejecuta el proceso de entrenamiento y validación interna conforme a la estrategia metodológica definida en el apartado 12.1. Se analizan las métricas de rendimiento y se ajustan los parámetros necesarios para garantizar estabilidad y coherencia del modelo.

El entregable de esta fase es un modelo validado en entorno experimental y preparado para su integración.

### 11.3 Fase 3 – Integración y desarrollo de la interfaz

En esta etapa se integra el modelo entrenado en la capa de presentación y se desarrolla la interfaz web para la introducción de variables y visualización de resultados. Se implementan mecanismos de validación de entradas y advertencias sobre el alcance del sistema.

El resultado esperado es un prototipo funcional completamente operativo dentro del alcance académico definido.

### 11.4 Fase 4 – Pruebas finales y documentación

La última fase contempla pruebas de funcionamiento integral del sistema, revisión de coherencia entre componentes y elaboración de la documentación técnica y académica definitiva. Se verifica que el sistema respeta los límites establecidos en los apartados de alcance, ética y legalidad.

El cierre de esta fase implica la consolidación del proyecto como artefacto académico completo y metodológicamente validado.

La planificación descrita no se entiende como un proceso estrictamente lineal, sino como un marco estructurado susceptible de iteración controlada. En caso de que los resultados obtenidos en la fase de validación no alcancen los criterios metodológicos definidos, se contempla el retorno a fases anteriores para ajustar el modelo o revisar el preprocesamiento de datos. Este enfoque refuerza la robustez del desarrollo y permite una gestión proactiva de riesgos técnicos.

## 12. Estrategia de desarrollo

La estrategia de desarrollo adoptada para GlucoCheck se fundamenta en un enfoque iterativo e incremental, alineado con el backlog definido y el plan de trabajo establecido. Este planteamiento permite construir el sistema por componentes funcionales claramente delimitados, validando cada uno de ellos antes de su integración completa.

### 12.1 Modelo de ciclo de vida

El ciclo de vida del proyecto se adopta bajo un enfoque iterativo e incremental, estructurado en iteraciones sucesivas que abarcan preparación de datos, modelado, integración y validación. Cada iteración genera un incremento funcional verificable, reduciendo la complejidad global del desarrollo y facilitando la detección temprana de desviaciones técnicas.

Este enfoque evita dependencias rígidas entre fases y permite ajustar decisiones técnicas en función de los resultados obtenidos en las etapas de validación.

### 12.2 Gestión de versiones y control de cambios

Durante el desarrollo se mantiene un control sistemático de versiones del código, la documentación y los artefactos generados. Cualquier modificación relevante en el pipeline de datos, en el modelo o en la interfaz se documenta y justifica, garantizando la trazabilidad de las decisiones técnicas adoptadas.

El control de cambios se orienta a preservar la coherencia entre el modelo entrenado, los datos utilizados y los resultados obtenidos, evitando inconsistencias derivadas de modificaciones no controladas.

### 12.3 Integración progresiva de componentes

La integración entre la capa de datos, el componente de modelado y la interfaz de usuario se realiza de forma progresiva. Antes de la integración definitiva, cada componente es validado de manera independiente, reduciendo el riesgo de errores acumulativos y facilitando la identificación de incidencias.

Este proceso contribuye a mantener la modularidad del sistema y favorece su mantenibilidad en un contexto académico.

### 12.4 Trazabilidad y coherencia metodológica

Se establece correspondencia explícita entre los objetivos definidos en el alcance, los elementos del backlog y los entregables generados en cada fase del plan de trabajo. Esta trazabilidad permite verificar que cada componente desarrollado responde a una necesidad previamente identificada y evita la incorporación de funcionalidades fuera del dominio definido.

En conjunto, la estrategia de desarrollo refuerza la solidez técnica del proyecto y garantiza la alineación entre diseño, implementación y validación.

### 12.5 Validación y control del modelo

Como parte de la estrategia de desarrollo, se establece un proceso formal de validación del modelo de clasificación orientado a garantizar su solidez metodológica y su coherencia con el alcance académico del proyecto. El conjunto de datos se organiza en subconjuntos diferenciados de entrenamiento y evaluación, evitando solapamientos que puedan comprometer la capacidad de generalización del sistema. Asimismo, se contemplan técnicas de validación cruzada con el fin de obtener estimaciones estables del rendimiento ante datos no observados.

La evaluación del modelo se apoya en métricas estándar en problemas de clasificación binaria, tales como la sensibilidad, la especificidad y la capacidad discriminativa global. Estas métricas permiten analizar el equilibrio entre la correcta identificación de perfiles de riesgo y la minimización de clasificaciones erróneas, en coherencia con la naturaleza del problema abordado.

Los resultados obtenidos se interpretan exclusivamente desde una perspectiva metodológica. No se realiza extrapolación a contextos clínicos reales sin validación externa adicional. En consecuencia, el proceso de validación se entiende como un mecanismo de control de calidad del modelo dentro del entorno experimental del proyecto.

## 13. Riesgos técnicos actualizados

El desarrollo del sistema GlucoCheck implica una serie de riesgos técnicos inherentes a los proyectos basados en modelos de aprendizaje automático. La identificación y gestión de estos riesgos forma parte del enfoque metodológico adoptado.

### 13.1 Riesgo de sobreajuste del modelo

Existe el riesgo de que el modelo de clasificación se ajuste en exceso a las particularidades del conjunto de datos de entrenamiento, reduciendo su capacidad de generalización ante datos no observados. Este riesgo se mitiga mediante técnicas de validación interna y control de estabilidad del rendimiento entre distintas particiones del dataset.

### 13.2 Riesgo de dependencia del conjunto de datos

El modelo se entrena sobre un dataset público específico, cuya estructura y distribución condicionan el comportamiento del sistema. Cambios en la composición de los datos o su aplicación a poblaciones con características diferentes podrían afectar al rendimiento del modelo, requiriendo procesos de validación externa y eventual recalibración.

### 13.3 Riesgo de deriva del modelo

En un contexto de uso prolongado o ante la incorporación futura de nuevos datos, podrían producirse cambios en la distribución de las variables que alteren la validez predictiva del modelo. Aunque el presente proyecto no contempla explotación en entorno real, se reconoce la necesidad de mecanismos de monitorización y actualización periódica en escenarios de aplicación extendida.

### 13.4 Riesgo de interpretabilidad limitada

Como ocurre en muchos modelos de clasificación supervisada, existe el riesgo de que los usuarios interpreten los resultados como determinaciones causales o diagnósticas. La mitigación de este riesgo se apoya en la delimitación clara del alcance, la inclusión de advertencias explícitas y la presentación comprensible de los resultados.

### 13.5 Riesgo de integración entre componentes

La separación modular entre la capa de datos, el modelo y la interfaz reduce la complejidad del sistema, pero introduce posibles riesgos de inconsistencias en la integración. Para mitigarlo, cada componente se valida de forma independiente antes de su integración definitiva.

En conjunto, la gestión de estos riesgos técnicos contribuye a reforzar la robustez del proyecto y su coherencia con el marco académico definido.

## 14. Repositorio del proyecto

El código fuente, la documentación técnica y los artefactos generados durante el desarrollo del proyecto se gestionan a través de un repositorio de control de versiones. Este repositorio centraliza los distintos componentes del sistema, incluyendo el pipeline de datos, el modelo de clasificación y la capa de presentación.

La estructura del repositorio se organiza de forma modular, diferenciando claramente los directorios correspondientes a datos, modelado, interfaz y documentación. Esta organización facilita la mantenibilidad del proyecto y permite una navegación clara entre los distintos elementos que lo componen.

Cada actualización relevante del sistema se registra mediante un sistema de versionado que permite rastrear cambios, recuperar estados anteriores y garantizar la trazabilidad de las decisiones técnicas adoptadas durante el desarrollo. Esta práctica contribuye a reforzar la reproducibilidad del proyecto y su coherencia metodológica.

El repositorio constituye, por tanto, el soporte técnico que consolida el proyecto como artefacto académico reproducible, transparente y verificable por terceros dentro del marco definido en la presente memoria.