import React from 'react';
import { SafeAreaView, Text, View, Button, FlatList } from 'react-native';

const pros = [
  { id: '1', name: 'Pro A', distance: '0.8 km' },
  { id: '2', name: 'Patrocinado: Loja Ferramentas', distance: 'Ad' },
  { id: '3', name: 'Pro B', distance: '1.2 km' },
];

export default function App() {
  return (
    <SafeAreaView style={{ flex: 1, padding: 16 }}>
      <Text style={{ fontSize: 24, fontWeight: '700' }}>EncontreAqui</Text>
      <Text>Busca por categoria + proximidade</Text>
      <Button title="Criar Solicitação" onPress={() => {}} />
      <FlatList
        data={pros}
        keyExtractor={(item) => item.id}
        renderItem={({ item }) => (
          <View style={{ paddingVertical: 12 }}>
            <Text>{item.name}</Text>
            <Text>{item.distance}</Text>
          </View>
        )}
      />
      <Text>Fluxos: Chat realtime, pagamento escrow, avaliações mútuas, notificações.</Text>
    </SafeAreaView>
  );
}
