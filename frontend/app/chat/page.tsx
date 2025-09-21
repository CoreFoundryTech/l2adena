"use client";

import { useState, useEffect, useRef } from "react";
import { useSearchParams } from "next/navigation";
import { useQuery } from "@tanstack/react-query";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

interface Room {
  room_id: string;
  other_user: string;
  last_message: string;
  last_message_time: string;
}

interface Message {
  id: number;
  room_id: string;
  sender_id: number;
  sender_username: string;
  content: string;
  created_at: string;
}

export default function ChatPage() {
  const searchParams = useSearchParams();
  const roomFromQuery = searchParams.get("room_id");
  const [selectedRoom, setSelectedRoom] = useState<string | null>(roomFromQuery);
  const [messages, setMessages] = useState<Message[]>([]);
  const [newMessage, setNewMessage] = useState("");
  const [ws, setWs] = useState<WebSocket | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const token = typeof window !== 'undefined' ? localStorage.getItem("token") : null;

  useEffect(() => {
    if (roomFromQuery) {
      setSelectedRoom(roomFromQuery);
    }
  }, [roomFromQuery]);

  const { data: rooms, isLoading } = useQuery<Room[]>({
    queryKey: ["chat-rooms"],
    queryFn: async () => {
      const response = await fetch("http://localhost:5001/chat/rooms", {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (!response.ok) throw new Error("Failed to fetch rooms");
      return response.json();
    },
    enabled: !!token,
  });

  const { data: roomMessages } = useQuery<Message[]>({
    queryKey: ["messages", selectedRoom],
    queryFn: async () => {
      if (!selectedRoom) return [];
      const response = await fetch(`http://localhost:5001/messages?room_id=${selectedRoom}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (!response.ok) throw new Error("Failed to fetch messages");
      return response.json();
    },
    enabled: !!selectedRoom && !!token,
  });

  useEffect(() => {
    if (roomMessages) {
      setMessages(roomMessages);
    }
  }, [roomMessages]);

  useEffect(() => {
    if (selectedRoom && token) {
      const websocket = new WebSocket(`ws://localhost:5001/ws/chat/${selectedRoom}?token=${token}`);
      websocket.onopen = () => {
        console.log("Connected to chat");
      };
      websocket.onmessage = (event) => {
        const message = JSON.parse(event.data);
        setMessages(prev => [...prev, message]);
      };
      websocket.onclose = () => {
        console.log("Disconnected from chat");
      };
      setWs(websocket);
      return () => {
        websocket.close();
      };
    }
  }, [selectedRoom, token]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const sendMessage = () => {
    if (ws && newMessage.trim()) {
      ws.send(JSON.stringify({ content: newMessage }));
      setNewMessage("");
    }
  };

  if (!token) return <div className="container mx-auto py-8">Debes iniciar sesión para acceder al chat.</div>;
  if (isLoading) return <div className="container mx-auto py-8">Cargando...</div>;

  return (
    <div className="container mx-auto py-8 h-screen flex">
      <div className="w-1/3 pr-4">
        <Card>
          <CardHeader>
            <CardTitle>Conversaciones</CardTitle>
          </CardHeader>
          <CardContent>
            {rooms?.map((room) => (
              <div
                key={room.room_id}
                className={`p-2 cursor-pointer rounded ${selectedRoom === room.room_id ? 'bg-blue-100' : 'hover:bg-gray-100'}`}
                onClick={() => setSelectedRoom(room.room_id)}
              >
                <div className="font-semibold">{room.other_user}</div>
                <div className="text-sm text-gray-600 truncate">{room.last_message}</div>
              </div>
            ))}
          </CardContent>
        </Card>
      </div>
      <div className="w-2/3 flex flex-col">
        <Card className="flex-1 flex flex-col">
          <CardHeader>
            <CardTitle>{selectedRoom ? `Chat con ${rooms?.find(r => r.room_id === selectedRoom)?.other_user}` : "Selecciona una conversación"}</CardTitle>
          </CardHeader>
          <CardContent className="flex-1 overflow-y-auto">
            {messages.map((msg) => (
              <div key={msg.id} className="mb-2">
                <strong>{msg.sender_username}:</strong> {msg.content}
                <div className="text-xs text-gray-500">{new Date(msg.created_at).toLocaleString()}</div>
              </div>
            ))}
            <div ref={messagesEndRef} />
          </CardContent>
          {selectedRoom && (
            <div className="p-4 border-t">
              <div className="flex gap-2">
                <Input
                  value={newMessage}
                  onChange={(e) => setNewMessage(e.target.value)}
                  placeholder="Escribe un mensaje..."
                  onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                />
                <Button onClick={sendMessage}>Enviar</Button>
              </div>
            </div>
          )}
        </Card>
      </div>
    </div>
  );
}