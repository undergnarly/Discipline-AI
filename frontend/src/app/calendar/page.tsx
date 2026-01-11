"use client";
import React from 'react';

// Заглушка для данных событий
const mockEvents = [
  { id: 1, title: 'Встреча с командой', start: '2025-06-10T10:00:00', end: '2025-06-10T11:00:00' },
  { id: 2, title: 'Обед', start: '2025-06-10T13:00:00', end: '2025-06-10T14:00:00' },
  { id: 3, title: 'Работа над проектом Discipline AI', start: '2025-06-10T14:30:00', end: '2025-06-10T17:00:00' },
];

export default function CalendarPage() {
  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-semibold">Календарь</h1>
        <button className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700">
          Добавить событие
        </button>
      </div>
      
      <div className="bg-white rounded-lg shadow">
        <ul className="divide-y divide-gray-200">
          {mockEvents.map(event => (
            <li key={event.id} className="p-4 hover:bg-gray-50">
              <p className="font-semibold text-gray-900">{event.title}</p>
              <p className="text-sm text-gray-500">
                {new Date(event.start).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})} - 
                {new Date(event.end).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}
              </p>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
} 