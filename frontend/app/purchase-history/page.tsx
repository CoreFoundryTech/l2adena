'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { useAuthStore } from "@/lib/store";

interface PurchaseHistory {
  id: number;
  buyer_id: number;
  listing_id: number;
  transaction_date: string;
  status: string;
  listing?: {
    server_name: string;
    chronicle: string;
    type: string;
    quantity: number;
    price: number;
  };
}

export default function PurchaseHistoryPage() {
  const [purchases, setPurchases] = useState<PurchaseHistory[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const { token, isAuthenticated } = useAuthStore();
  const router = useRouter();

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/auth/login');
      return;
    }

    const fetchPurchases = async () => {
      try {
        const response = await fetch('http://localhost:5001/purchase-history/me', {
          headers: { 'Authorization': `Bearer ${token}` },
        });
        if (response.ok) {
          const data = await response.json();
          // For each purchase, fetch listing details
          const purchasesWithListings = await Promise.all(
            data.map(async (purchase: PurchaseHistory) => {
              try {
                const listingRes = await fetch(`http://localhost:5001/listings/${purchase.listing_id}`);
                if (listingRes.ok) {
                  const listing = await listingRes.json();
                  return { ...purchase, listing };
                }
              } catch (err) {
                // Ignore errors for individual listings
              }
              return purchase;
            })
          );
          setPurchases(purchasesWithListings);
        } else {
          setError('Failed to load purchase history');
        }
      } catch (err) {
        setError('Network error');
      } finally {
        setLoading(false);
      }
    };

    fetchPurchases();
  }, [token, isAuthenticated, router]);

  if (!isAuthenticated) return null;
  if (loading) return <div className="container mx-auto py-8">Loading...</div>;
  if (error) return <div className="container mx-auto py-8 text-red-500">{error}</div>;

  return (
    <div className="container mx-auto py-8">
      <h1 className="text-3xl font-bold mb-6">Purchase History</h1>
      {purchases.length === 0 ? (
        <p>No purchases yet.</p>
      ) : (
        <div className="grid gap-4">
          {purchases.map((purchase) => (
            <Card key={purchase.id}>
              <CardHeader>
                <CardTitle>{purchase.listing?.server_name || 'Unknown Listing'}</CardTitle>
                <CardDescription>
                  {purchase.listing?.chronicle} - {purchase.listing?.type} - {purchase.listing?.quantity} units
                </CardDescription>
              </CardHeader>
              <CardContent>
                <p>Price: ${purchase.listing?.price}</p>
                <p>Status: {purchase.status}</p>
                <p>Date: {new Date(purchase.transaction_date).toLocaleDateString()}</p>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}