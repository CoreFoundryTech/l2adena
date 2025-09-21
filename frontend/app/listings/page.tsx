"use client";

import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import Link from "next/link";
import { ListingCard } from "@/components/ListingCard";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { ServerSelect } from "@/components/ServerSelect";

interface Listing {
  id: number;
  server_id: number;
  chronicle: string;
  type: string;
  quantity: number;
  price: number;
  description?: string;
  status: string;
  is_featured: boolean;
  featured_expires_at?: string;
  created_at: string;
  seller_id: number;
}

interface Filters {
  server_id: string;
  chronicle: string;
  type: string;
  price_min: string;
  price_max: string;
  quantity_min: string;
  quantity_max: string;
  description_search: string;
}

export default function ListingsPage() {
  const [filters, setFilters] = useState<Filters>({
    server_id: "",
    chronicle: "",
    type: "",
    price_min: "",
    price_max: "",
    quantity_min: "",
    quantity_max: "",
    description_search: "",
  });

  const queryParams = new URLSearchParams();
  Object.entries(filters).forEach(([key, value]) => {
    if (value) queryParams.set(key, value);
  });

  const { data: listings, isLoading, error } = useQuery<Listing[]>({
    queryKey: ["listings", filters],
    queryFn: async () => {
      const response = await fetch(`http://localhost:5001/listings?${queryParams}`);
      if (!response.ok) throw new Error("Failed to fetch listings");
      return response.json();
    },
  });

  const handleFilterChange = (field: keyof Filters, value: string) => {
    setFilters(prev => ({ ...prev, [field]: value }));
  };

  const clearFilters = () => {
    setFilters({
      server_id: "",
      chronicle: "",
      type: "",
      price_min: "",
      price_max: "",
      quantity_min: "",
      quantity_max: "",
      description_search: "",
    });
  };

  if (isLoading) return <div className="container mx-auto py-8">Cargando...</div>;
  if (error) return <div className="container mx-auto py-8">Error al cargar listings</div>;

  return (
    <div className="container mx-auto py-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Anuncios</h1>
        <Link href="/listings/create">
          <Button>Crear Anuncio</Button>
        </Link>
      </div>

      {/* Filters */}
      <div className="bg-gray-50 p-4 rounded-lg mb-6">
        <h2 className="text-lg font-semibold mb-4">Filtros</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <div>
            <Label htmlFor="server_id">Servidor</Label>
            <ServerSelect
              value={filters.server_id ? parseInt(filters.server_id) : undefined}
              onValueChange={(value) => handleFilterChange("server_id", value.toString())}
              placeholder="Seleccionar servidor"
            />
          </div>
          <div>
            <Label htmlFor="chronicle">Crónica</Label>
            <Input
              id="chronicle"
              value={filters.chronicle}
              onChange={(e) => handleFilterChange("chronicle", e.target.value)}
              placeholder="Crónica"
            />
          </div>
          <div>
            <Label htmlFor="type">Tipo</Label>
            <Select value={filters.type || "all"} onValueChange={(value) => handleFilterChange("type", value === "all" ? "" : value)}>
              <SelectTrigger>
                <SelectValue placeholder="Todos" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">Todos</SelectItem>
                <SelectItem value="BUY">Comprar</SelectItem>
                <SelectItem value="SELL">Vender</SelectItem>
              </SelectContent>
            </Select>
          </div>
          <div>
            <Label htmlFor="description_search">Buscar en descripción</Label>
            <Input
              id="description_search"
              value={filters.description_search}
              onChange={(e) => handleFilterChange("description_search", e.target.value)}
              placeholder="Palabras clave"
            />
          </div>
          <div>
            <Label htmlFor="price_min">Precio mínimo</Label>
            <Input
              id="price_min"
              type="number"
              value={filters.price_min}
              onChange={(e) => handleFilterChange("price_min", e.target.value)}
              placeholder="0"
            />
          </div>
          <div>
            <Label htmlFor="price_max">Precio máximo</Label>
            <Input
              id="price_max"
              type="number"
              value={filters.price_max}
              onChange={(e) => handleFilterChange("price_max", e.target.value)}
              placeholder="1000"
            />
          </div>
          <div>
            <Label htmlFor="quantity_min">Cantidad mínima</Label>
            <Input
              id="quantity_min"
              type="number"
              value={filters.quantity_min}
              onChange={(e) => handleFilterChange("quantity_min", e.target.value)}
              placeholder="1"
            />
          </div>
          <div>
            <Label htmlFor="quantity_max">Cantidad máxima</Label>
            <Input
              id="quantity_max"
              type="number"
              value={filters.quantity_max}
              onChange={(e) => handleFilterChange("quantity_max", e.target.value)}
              placeholder="100"
            />
          </div>
        </div>
        <div className="mt-4">
          <Button variant="outline" onClick={clearFilters}>Limpiar Filtros</Button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {listings?.map((listing) => (
          <ListingCard key={listing.id} {...listing} />
        ))}
      </div>
    </div>
  );
}