let pass = 1
const passInitial = 1
const passEnd = 3
const cita = {
    id:'',
    nombre: '',
    fecha: '',
    hora: '',
    servicios: []  
}


window.document.addEventListener("DOMContentLoaded",()=>{
    startApp();
})

const startApp = () => {
    showSection();// show and hide sections
    tabs();//change the sectiom when press the tab
    botonsPagination();// add o remove the botons paginators
    pageBack();
    pageNext();
    queryAPI();
    nameClient();// add name client the object of cita
    selectionFecha();// add the fecha in the object
    selectionHora();// add the hora in the object
    idClient();
    showResumen();// show resumen turno
}
function showSection(){
// hide sections
    const previousSection = document.querySelector('.mostrar');
    if(previousSection){
        previousSection.classList.remove('mostrar');
    }
// Selection the section with pass
    const section = window.document.querySelector(`#paso-${pass}`);
    section.classList.add('mostrar');

//remove the class actual the previous tab
    const previousTab = window.document.querySelector('.actual')
    if( previousTab ){
        previousTab.classList.remove('actual')
    }
//resalt the tab actual
    const tab = document.querySelector(`[data-paso="${pass}"]`);
    tab.classList.add('actual');
}

const tabs = () => {
    // const botones = document.querySelectorAll('.tabs button')// este devuelve un node lista que se parece a un array pero no tine metodos como un array
/** como yo quiero delegar eventos a multiples elementos se lo puede hacer de dos maneras una es con for each */
    // botones.forEach(( elements ) => {
    //     elements.addEventListener("click",(e)=>{
    //         console.log("eeeee")
    //     })
    // })
// y tenemos esta opcion que es la mas recomendable y eficiente esta tecnica de delegacion se llama  (event bubbling)
    window.addEventListener("click",(e) => {
        // console.log(e.target)//target es aque le dimos click
        if(e.target.matches(".tabs button")){// aca seleccionamos el elementos que queremos matchear
            // console.log(Number(e.target.dataset.paso))//data set es donde se guardan las propiedades personalizadas que le colocamos a nuestros elementos html
        //para poder crear tus propieas propiedades personalizadas en una etiqueta html deves poner data-nombreDeLaPropiedadPersonalizada
        pass = Number(e.target.dataset.paso);
        showSection();
        botonsPagination();
    }
    });
}

const botonsPagination = () =>{
    const pageNext = window.document.querySelector('#siguiente')
    const pageBack = window.document.querySelector('#anterior')
    if(pass == 1){
        pageNext.classList.remove("ocultar")
        pageBack.classList.add("ocultar")
    }else if(pass == 3){
        pageBack.classList.remove("ocultar")
        pageNext.classList.add("ocultar")
        showResumen()
    }else{
        pageNext.classList.remove("ocultar")
        pageBack.classList.remove("ocultar")
    }
    showSection()
}
function pageBack(){
    // console.log("me ejcutoooo")
    const backPage = document.querySelector('#anterior')
    backPage.addEventListener('click',() => {
        if(pass <= passInitial)return;
        pass = pass - 1;
        botonsPagination()
    })
}
function pageNext(){
    const nextPage = document.querySelector('#siguiente')
    nextPage.addEventListener('click',() => {
        console.log("ejecutandoooo")
        if(pass >= passEnd)return;
        pass = pass + 1;
        botonsPagination()
    })
}

async function queryAPI() {
    try {
        const url = 'http://127.0.0.1:8000/landing/api/servicios'
        const response  = await fetch(url)
        const dataResponse = await response.json()
        showServicios(dataResponse);
        // console.log(dataResponse)
    } catch (error) {
        console.log(error)
    }
}
function showServicios(servicios){
    servicios.forEach(servicio =>{
        const {id, nombre, precio}  = servicio;
        const nameServicios = document.createElement('P');
        nameServicios.classList.add('nombre-servicio');
        nameServicios.textContent = nombre;

        const priceServicio = document.createElement('P');
        priceServicio.classList.add('precio-servicio');
        priceServicio.textContent = `$${precio}`;

        const servicioDiv = document.createElement('DIV');
        servicioDiv.classList.add('servicio');
        servicioDiv.dataset.idServicios = id ;// estp sirve para crear una propiedad personalizada dentro del tags
        servicioDiv.onclick = function(){
            selectionService(servicio)
        }

        servicioDiv.appendChild(nameServicios);
        servicioDiv.appendChild(priceServicio);

        document.querySelector('#servicios').appendChild(servicioDiv)
        
        
    })
}
 function selectionService(servicio){
    const { id } = servicio;
    const { servicios } = cita;

    //comprobate if a service exits or are add
    if( servicios.some( agregado => agregado.id === id ) ){
        cita.servicios = servicios.filter(agregado => agregado.id !== id )
        const divServicio = document.querySelector(`[data-id-servicios="${id}"]`);
        divServicio.classList.remove('seleccionado');
    }else{
        cita.servicios = [...servicios, servicio];
        const divServicio = document.querySelector(`[data-id-servicios="${id}"]`);
        divServicio.classList.add('seleccionado');
    }
 }

 function nameClient(){
    const name = document.querySelector('#nombre').value;
    cita.nombre = name; 
 }

function selectionFecha() {
    const inputFecha = window.document.querySelector('#fecha')
    console.log(inputFecha)
    inputFecha.addEventListener('input',function(e){
        console.log(e.target.value);
        const dia = new Date(e.target.value).getUTCDay();//obtengo un numero del dia ejemplo hoy es sabado por ende me va a dar un numero 5
        if([6,0].includes(dia)){
            e.target.value = '';
            showAlert('SABADO Y DOMINGO  NO SELECCIONABLE','errores','.formulario');
        }else{
            cita.fecha = e.target.value;
            console.log(cita)
        }
    })
}
function selectionHora(){
    const inputHora = window.document.querySelector('#hora');
    inputHora.addEventListener('input', function(e){
        const horaCita = e.target.value;
        const hora = horaCita.split(":")[0];
        if(hora < 10 || hora > 18){
            showAlert('Hora no validas', 'errores','.formulario')
        }else{
            cita.hora = e.target.value
        }
    })
}

function showAlert(mensaje, tipo, elemento, desactivate = true) {
    const alertPrev = document.querySelector('.alerta');
    if(alertPrev) {
        alertPrev.remove()
    };
    const alert = window.document.createElement('DIV');
    alert.textContent = mensaje;
    alert.classList.add('alerta');
    alert.classList.add(tipo);

    const formulario = document.querySelector(elemento);
    formulario.appendChild(alert);
    if(desactivate){
        setTimeout(()=>{
            alert.remove();
        },3000);
    }
    
}

function showResumen(){
    console.log("me ejecutoo")
    const resumen = document.querySelector('.contenido-resumen');
    //clear the content of resumen
    while (resumen.firstChild) {
        resumen.removeChild(resumen.firstChild);
    }
    console.log(Object.values(cita));
    if(Object.values(cita).includes(' ') || cita.servicios.length === 0){
        showAlert('faltan datos de Servicios, Fecha u Hora', 'errores','.contenido-resumen', false)
        return;
    }
    // formantear el div de resumen
      //Heading para Servicios en resumen
    const title = document.createElement('H3');
    title.textContent = 'Tu resumen de servicios';
    resumen.appendChild(title);
    const { nombre, fecha, hora, servicios } = cita
    const nameClient = document.createElement('P');
    nameClient.innerHTML = `<span>Nombre:</span>${nombre}`;

    const fechaCita = document.createElement('P');
    fechaCita.innerHTML = `<span>Fecha:</span>${fecha}`

    const horaCita = document.createElement('P');
    horaCita.innerHTML = `<span>Hora:</span>${hora} Horas`

    // iterando y mostrando los servicios
    servicios.forEach(servicio => {
        const { id, precio, nombre } = servicio;
        const contendorServicio = window.document.createElement('DIV');
        contendorServicio.classList.add('contenedor-servicio');

        const textoServicio = window.document.createElement('P');
        textoServicio.textContent = nombre;

        const precioServicio = window.document.createElement('P');
        precioServicio.innerHTML = `<span>Precio:</span> $${precio}`;

        contendorServicio.appendChild(textoServicio);
        contendorServicio.appendChild(precioServicio);

        resumen.appendChild(contendorServicio);
    })
    
    //Heading para Servicios en resumen
    const headingServices = document.createElement('H3');
    headingServices.textContent = 'Tu resumen de tu turno';
    resumen.appendChild(headingServices);
    resumen.appendChild(nameClient)
    resumen.appendChild(fechaCita)
    resumen.appendChild(horaCita)
    //Boton para crear una cita
    const botnReservar = window.document.createElement('Button');
    botnReservar.classList.add('boton');
    botnReservar.textContent = 'Reservar Turno';
    botnReservar.onclick = reservarTurno;
    resumen.appendChild(botnReservar);
}

async function reservarTurno(){
    const { nombre,fecha, hora, servicios, id} = cita;
    const idServicios = servicios.map(servicio=> servicio.id)
    const datos = new FormData();
    datos.append('usuarioId', id);
    datos.append('fecha', fecha);
    datos.append('hora', hora);
    datos.append('servcio',idServicios)   
    try {
        const url = 'http://127.0.0.1:8000/landing/api/turnos'
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        console.log("este es el token",csrfToken)
        const respuesta =  await fetch(url,{
            method:'POST',
            headers: {'X-CSRFToken': csrfToken},
            body:datos
        })
        const respuestaJson = await respuesta.json()
        if(respuestaJson.resultado){
            Swal.fire({
                icon: 'success',
                title: 'Turno Creado',
                text: 'Tu turno fue crado con exito',
                button: 'OK'
              }).then(()=>{
                setTimeout(()=>{
                    window.location.reload();

                },700)
              })
        }
        
    } catch (error) {
        Swal.fire({
            icon: 'error',
            title: 'Surgio un error ',
            text: 'Hubo un error al guardar tu turno',
          })
          
    }

    

}

function idClient(){
    console.log(Number(document.querySelector('#iduser').value))
    cita.id = Number(document.querySelector('#iduser').value);
}