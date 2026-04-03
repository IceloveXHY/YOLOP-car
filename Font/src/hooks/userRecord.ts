import { ref } from 'vue'

// 符合规范的命名，以 use 开头
export const useRecords = () => {
    const records = ref([
        {
            title: '疲劳驾驶',
            description: '道路千万条，安全第一条',
            time: '2025-4-15 09:15'
        },
        {
            title: '抛洒物检测',
            description: '禁止乱扔!!',
            time: '2025-4-5 14:30'
        },
        {
            title: '车辆违停',
            description: '处罚',
            time: '2025-4-25 11:00'
        },
        {
            title: '道路生成',
            description: '生成式检测',
            time: '2025-4-20 16:45'
        },
    ])

    return {
        records
    }
}