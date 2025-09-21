'use client';

import { useQuery } from '@tanstack/react-query';
import { ServerActivityCard } from '@/components/ServerActivityCard';

interface ServerActivity {
  id: number;
  name: string;
  chronicle: string;
  active_listings: number;
  total_transactions: number;
  total_sellers: number;
}

export default function ServersPage() {
  const { data: servers, isLoading, error } = useQuery({
    queryKey: ['servers-activity'],
    queryFn: async () => {
      const response = await fetch('http://localhost:5001/servers/activity');
      if (!response.ok) {
        throw new Error('Failed to fetch servers activity');
      }
      return response.json() as Promise<ServerActivity[]>;
    },
  });

  if (isLoading) {
    return <div className="container mx-auto p-4">Cargando servidores...</div>;
  }

  if (error) {
    return <div className="container mx-auto p-4">Error al cargar servidores: {error.message}</div>;
  }

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-6">Actividad de Servidores</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {servers?.map((server) => (
          <ServerActivityCard
            key={server.id}
            id={server.id}
            name={server.name}
            chronicle={server.chronicle}
            active_listings={server.active_listings}
            total_transactions={server.total_transactions}
            total_sellers={server.total_sellers}
          />
        ))}
      </div>
    </div>
  );
}