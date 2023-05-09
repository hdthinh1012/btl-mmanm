# BTL MMANM

# Hướng dẫn chạy chương trình
```bash
cd srcs
python3 main.py -h # Hướng dẫn các tham số cần thiết
```

## Chạy mode encryption
```bash 
python main.py enc --inp <input_file> --out <output_file> {caesar,railfence,mix} <key>
```

## Chạy mode decryption
```bash 
python main.py enc --inp <input_file> --out <output_file> {caesar,railfence,mix} <key>
```

## Chạy mode crack (brute force tìm key và plaintext)
```bash 
python main.py crk --inp <input_file> --out <output_file> --cipher {caesar,railfence,mix}

python main.py crk --inp <input_file> --out <output_file> # Crack random cipher without knowing cipher algorithm
```
