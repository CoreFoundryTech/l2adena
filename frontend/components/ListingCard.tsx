import Link from "next/link";
import { useRouter } from "next/navigation";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";

interface ListingCardProps {
  id: number;
  server_id: number;
  chronicle: string;
  type: string;
  quantity: number;
  price: number;
  description?: string;
  is_featured: boolean;
  created_at: string;
  seller_id: number;
}

export function ListingCard({ id, server_id, chronicle, type, quantity, price, description, is_featured, seller_id }: ListingCardProps) {
  const router = useRouter();
  const token = typeof window !== 'undefined' ? localStorage.getItem("token") : null;
  const isLoggedIn = !!token;

  const handleContact = async () => {
    if (!token) return;
    try {
      const response = await fetch("http://localhost:5001/chat/start", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ listing_id: id }),
      });
      if (response.ok) {
        const { room_id } = await response.json();
        router.push(`/chat?room_id=${room_id}`);
      }
    } catch (error) {
      console.error("Error starting chat:", error);
    }
  };

  return (
    <Card className="w-full max-w-sm">
      <CardHeader>
        <div className="flex justify-between items-start">
          <CardTitle className="text-lg">Server {server_id} - {chronicle}</CardTitle>
          <div className="flex gap-2">
            {is_featured && <Badge variant="default">Destacado</Badge>}
            <Badge variant="secondary">{type}</Badge>
          </div>
        </div>
        <CardDescription>{description || "Sin descripción"}</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="flex justify-between items-center">
          <div>
            <span className="text-2xl font-bold">${price}</span>
            <p className="text-sm text-gray-600">Cantidad: {quantity}</p>
          </div>
          <div className="flex gap-2">
            <Link href={`/listings/${id}`}>
              <Button variant="outline">Ver Detalles</Button>
            </Link>
            {isLoggedIn && (
              <>
                <Button onClick={handleContact} variant="secondary">Contactar</Button>
                <Link href={`/listings/${id}/edit`}>
                  <Button variant="outline" size="sm">Editar</Button>
                </Link>
              </>
            )}
          </div>
        </div>
      </CardContent>
    </Card>
  );
}