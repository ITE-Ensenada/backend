import { Poppins } from "next/font/google";
import Image from 'next/image';
import perfil from 'app/img/foto.jpg';

const inter = Poppins({ weight: '400', subsets: ['latin'] })

function About() {
    return (
        <div className="bg-secondary h-screen w-full" >
            <h1 className="text-black text-center m-5">Soy el about</h1>

            <div className="container mx-auto p-8 bg-terciary rounded-sm">
                <h2 className="text-2xl font-bold mb-4">Perfil profesional</h2>
                <div className="flex items-center">
                    <p className="w-1/2 pr-4">Mi nombre es alan cordova viera estudio sistemas computacionales <br /> domino todos los lenguajes de programacion.</p>
                    <p className="w-1/2 pr-4">Lorem ipsum dolor sit amet consectetur adipisicing elit.
                        Nemo minima, fugit corrupti magnam quod quia impedit ipsa commodi molestiae voluptas ut ullam molestias sequi iusto officia vero maiores quasi expedita?</p>
                    <Image src={perfil} className="h-50 w-52" alt='' />
                </div>
            </div>

        </div >



    );

}

export default About;