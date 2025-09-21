'use client';

import { useAuthStore } from "@/lib/store";

export default function PremiumPage() {
  const { isAuthenticated } = useAuthStore();

  return (
    <div className="container mx-auto py-8">
      <h1 className="text-3xl font-bold mb-6">Servicios Premium</h1>
      <p className="mb-6 text-gray-600">
        Descubre las ventajas de nuestros servicios premium para vendedores verificados.
      </p>

      <div className="grid md:grid-cols-2 gap-6">
        {/* Destacar Anuncios */}
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-xl font-semibold mb-4">Destacar Anuncios</h2>
          <p className="mb-4">
            Haz que tus anuncios se destaquen en las búsquedas y aparezcan primero en la lista.
          </p>
          <ul className="list-disc list-inside mb-4">
            <li>Posición prioritaria en búsquedas</li>
            <li>Badge de "Destacado" visible</li>
            <li>Mayor visibilidad para compradores</li>
            <li>Duración configurable (1-30 días)</li>
          </ul>
          {!isAuthenticated ? (
            <p className="text-sm text-gray-500">Inicia sesión para acceder a esta función.</p>
          ) : (
            <button className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">
              Próximamente - Integración con Stripe
            </button>
          )}
        </div>

        {/* Verificación de Vendedor */}
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-xl font-semibold mb-4">Verificación de Vendedor</h2>
          <p className="mb-4">
            Obtén el badge de vendedor verificado para generar más confianza en los compradores.
          </p>
          <ul className="list-disc list-inside mb-4">
            <li>Badge azul de verificación en perfil</li>
            <li>Mayor confianza de compradores</li>
            <li>Acceso prioritario al soporte</li>
            <li>Estadísticas avanzadas de ventas</li>
          </ul>
          {!isAuthenticated ? (
            <p className="text-sm text-gray-500">Inicia sesión para acceder a esta función.</p>
          ) : (
            <button className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600">
              Próximamente - Integración con Stripe
            </button>
          )}
        </div>

        {/* Suscripción Premium */}
        <div className="bg-white p-6 rounded-lg shadow-md md:col-span-2">
          <h2 className="text-xl font-semibold mb-4">Suscripción Premium Mensual</h2>
          <p className="mb-4">
            Accede a todas las funciones premium con una suscripción mensual.
          </p>
          <div className="grid md:grid-cols-3 gap-4">
            <div className="border p-4 rounded">
              <h3 className="font-semibold">Básico</h3>
              <p className="text-2xl font-bold">$9.99/mes</p>
              <ul className="list-disc list-inside mt-2">
                <li>5 destacados por mes</li>
                <li>Verificación básica</li>
                <li>Soporte estándar</li>
              </ul>
            </div>
            <div className="border p-4 rounded border-blue-500">
              <h3 className="font-semibold">Pro</h3>
              <p className="text-2xl font-bold">$19.99/mes</p>
              <ul className="list-disc list-inside mt-2">
                <li>Destacados ilimitados</li>
                <li>Verificación premium</li>
                <li>Soporte prioritario</li>
                <li>Análisis avanzados</li>
              </ul>
            </div>
            <div className="border p-4 rounded">
              <h3 className="font-semibold">Enterprise</h3>
              <p className="text-2xl font-bold">$49.99/mes</p>
              <ul className="list-disc list-inside mt-2">
                <li>Todo lo de Pro</li>
                <li>API access</li>
                <li>Gestión de equipo</li>
                <li>Soporte 24/7</li>
              </ul>
            </div>
          </div>
          {!isAuthenticated ? (
            <p className="text-sm text-gray-500 mt-4">Inicia sesión para suscribirte.</p>
          ) : (
            <button className="bg-purple-500 text-white px-6 py-3 rounded hover:bg-purple-600 mt-4">
              Próximamente - Integración con Stripe
            </button>
          )}
        </div>
      </div>

      <div className="mt-8 bg-gray-100 p-6 rounded-lg">
        <h2 className="text-xl font-semibold mb-4">¿Por qué elegir Premium?</h2>
        <div className="grid md:grid-cols-3 gap-4">
          <div className="text-center">
            <h3 className="font-semibold">Más Visibilidad</h3>
            <p>Tus anuncios se verán primero, aumentando las ventas.</p>
          </div>
          <div className="text-center">
            <h3 className="font-semibold">Confianza</h3>
            <p>Los compradores confían más en vendedores verificados.</p>
          </div>
          <div className="text-center">
            <h3 className="font-semibold">Soporte</h3>
            <p>Acceso a soporte prioritario y herramientas avanzadas.</p>
          </div>
        </div>
      </div>
    </div>
  );
}