import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

interface ServerActivityCardProps {
  id: number;
  name: string;
  chronicle: string;
  active_listings: number;
  total_transactions: number;
  total_sellers: number;
}

export function ServerActivityCard({
  id,
  name,
  chronicle,
  active_listings,
  total_transactions,
  total_sellers,
}: ServerActivityCardProps) {
  return (
    <Card className="w-full max-w-md">
      <CardHeader>
        <CardTitle className="text-lg">{name}</CardTitle>
        <p className="text-sm text-gray-600">Crónica: {chronicle}</p>
      </CardHeader>
      <CardContent>
        <div className="space-y-2">
          <div className="flex justify-between">
            <span>Anuncios activos:</span>
            <span className="font-semibold">{active_listings}</span>
          </div>
          <div className="flex justify-between">
            <span>Total transacciones:</span>
            <span className="font-semibold">{total_transactions}</span>
          </div>
          <div className="flex justify-between">
            <span>Total vendedores:</span>
            <span className="font-semibold">{total_sellers}</span>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}