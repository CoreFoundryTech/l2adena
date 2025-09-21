import { useServers } from '@/lib/api';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';

interface ServerSelectProps {
  value?: number;
  onValueChange: (value: number) => void;
  placeholder?: string;
}

export function ServerSelect({ value, onValueChange, placeholder = "Seleccionar servidor" }: ServerSelectProps) {
  const { data: servers, isLoading, error } = useServers();

  if (isLoading) {
    return (
      <Select disabled>
        <SelectTrigger>
          <SelectValue placeholder="Cargando servidores..." />
        </SelectTrigger>
      </Select>
    );
  }

  if (error) {
    return (
      <Select disabled>
        <SelectTrigger>
          <SelectValue placeholder="Error al cargar servidores" />
        </SelectTrigger>
      </Select>
    );
  }

  return (
    <Select value={value?.toString()} onValueChange={(val) => onValueChange(parseInt(val))}>
      <SelectTrigger>
        <SelectValue placeholder={placeholder} />
      </SelectTrigger>
      <SelectContent>
        {servers?.map((server: any) => (
          <SelectItem key={server.id} value={server.id.toString()}>
            {server.name} ({server.chronicle})
          </SelectItem>
        ))}
      </SelectContent>
    </Select>
  );
}