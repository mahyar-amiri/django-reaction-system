// /* @type {import('tailwindcss').Config} */
tailwind.config = {
    darkMode: ['class', '[data-mode="dark"]'],
    content: [
        '../../templates/**/*.html',
    ],
    theme: {
        extend: {
            colors: {
                // LIGHT
                'react-default-bg-light': '#f3f4f6',
                'react-default-border-light': '#e5e7eb',
                'react-selected-bg-light': '#dbeafe',
                'react-selected-border-light': '#bfdbfe',
                'react-count-text-light': '#000000',

                // DARK
                'react-default-bg-dark': '#334155',
                'react-default-border-dark': '#6b7280',
                'react-selected-bg-dark': '#64748b',
                'react-selected-border-dark': '#1e293b',
                'react-count-text-dark': '#f3f4f6',
            },
        },
    },
    plugins: [],
}
