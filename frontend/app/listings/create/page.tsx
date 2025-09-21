"use client";

import { useState } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ServerSelect } from "@/components/ServerSelect";

interface CreateListingForm {
  server_id: number;
  chronicle: string;
  type: "BUY" | "SELL";
  quantity: number;
  price: number;
  description: string;
  is_featured: boolean;
}

export default function CreateListingPage() {
  const router = useRouter();
  const queryClient = useQueryClient();
  const [form, setForm] = useState<CreateListingForm>({
    server_id: 0,
    chronicle: "",
    type: "SELL",
    quantity: 1,
    price: 0,
    description: "",
    is_featured: false,
  });
  const [errors, setErrors] = useState<Record<string, string>>({});

  const createListingMutation = useMutation({
    mutationFn: async (data: CreateListingForm) => {
      const token = localStorage.getItem("token");
      const response = await fetch("http://localhost:5001/listings", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(data),
      });
      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || "Error al crear anuncio");
      }
      return response.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["listings"] });
      router.push("/listings");
    },
    onError: (error: Error) => {
      alert(error.message);
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const newErrors: Record<string, string> = {};

    if (!form.server_id) newErrors.server_id = "Servidor requerido";
    if (!form.chronicle.trim()) newErrors.chronicle = "Crónica requerida";
    if (form.quantity <= 0) newErrors.quantity = "Cantidad debe ser mayor a 0";
    if (form.price <= 0) newErrors.price = "Precio debe ser mayor a 0";

    setErrors(newErrors);
    if (Object.keys(newErrors).length === 0) {
      createListingMutation.mutate(form);
    }
  };

  const handleChange = (field: keyof CreateListingForm, value: string | number | boolean) => {
    setForm(prev => ({ ...prev, [field]: value }));
    if (errors[field]) {
      setErrors(prev => {
        const newErrors = { ...prev };
        delete newErrors[field];
        return newErrors;
      });
    }
  };

  return (
    <div className="container mx-auto py-8">
      <Card className="max-w-2xl mx-auto">
        <CardHeader>
          <CardTitle>Crear Nuevo Anuncio</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <Label htmlFor="server_id">Servidor</Label>
              <ServerSelect
                value={form.server_id}
                onValueChange={(value) => handleChange("server_id", value)}
                placeholder="Seleccionar servidor"
              />
              {errors.server_id && <p className="text-red-500 text-sm">{errors.server_id}</p>}
            </div>

            <div>
              <Label htmlFor="chronicle">Crónica</Label>
              <Input
                id="chronicle"
                value={form.chronicle}
                onChange={(e) => handleChange("chronicle", e.target.value)}
                required
              />
              {errors.chronicle && <p className="text-red-500 text-sm">{errors.chronicle}</p>}
            </div>

            <div>
              <Label htmlFor="type">Tipo</Label>
              <Select value={form.type} onValueChange={(value: "BUY" | "SELL") => handleChange("type", value)}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="SELL">Vender</SelectItem>
                  <SelectItem value="BUY">Comprar</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div>
              <Label htmlFor="quantity">Cantidad</Label>
              <Input
                id="quantity"
                type="number"
                min="1"
                value={form.quantity}
                onChange={(e) => handleChange("quantity", parseInt(e.target.value) || 1)}
                required
              />
              {errors.quantity && <p className="text-red-500 text-sm">{errors.quantity}</p>}
            </div>

            <div>
              <Label htmlFor="price">Precio</Label>
              <Input
                id="price"
                type="number"
                min="0.01"
                step="0.01"
                value={form.price}
                onChange={(e) => handleChange("price", parseFloat(e.target.value) || 0)}
                required
              />
              {errors.price && <p className="text-red-500 text-sm">{errors.price}</p>}
            </div>

            <div>
              <Label htmlFor="description">Descripción</Label>
              <Textarea
                id="description"
                value={form.description}
                onChange={(e) => handleChange("description", e.target.value)}
                rows={4}
              />
            </div>

            <div className="flex items-center space-x-2">
              <input
                type="checkbox"
                id="is_featured"
                checked={form.is_featured}
                onChange={(e) => handleChange("is_featured", e.target.checked)}
              />
              <Label htmlFor="is_featured">Destacar anuncio (Próximamente con pago)</Label>
            </div>

            <Button type="submit" disabled={createListingMutation.isPending}>
              {createListingMutation.isPending ? "Creando..." : "Crear Anuncio"}
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}