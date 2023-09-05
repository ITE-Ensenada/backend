import Link from "next/link";

const menuRoutes = [{
    ruta: '/',
    nombre: 'Inicio',
}, {
    ruta: '/about',
    nombre: 'Acerca de'
},
{
    ruta: '/composicion_corporal',
    nombre: 'Composicion'
}
]

function Menu() {
    return (
        <div className="w-[20%] bg-primary h-screen py-8 px-4">
            <h1 className="text-white text-center mb-10 text-2xl font-semibold">Menu</h1>
            <ol className="space-y-2">
                {menuRoutes.map((menu, key) => (
                    <li key={key}>
                        <Link href={menu.ruta} className="text-white block py-2 px-4 rounded-md text-white hover:bg-secondary transition duration-300">
                            {menu.nombre}
                        </Link>
                    </li>
                ))}
            </ol>
        </div>
    );

}

export default Menu;