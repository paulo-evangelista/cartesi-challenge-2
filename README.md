# Code Challenge 2 - Cartesi <> Inteli masterclass

desafio: [henriquemarlon/cartesi-code-challenge-2](https://github.com/henriquemarlon/cartesi-code-challenge-2/tree/main)

https://github.com/paulo-evangelista/cartesi-challenge-2/assets/99093520/ae86c29b-5c51-4cab-a2bc-11fc92f2ed90

## Qual era o input correto?
`{"guess":3, "birth_year_minus_the_guess": 1593}`

- O apelido "cartesians" vem do nome de René Descartes,que nasceu em 1596
- A desassemblagem do binário dentro do Dapp mostra que, para a função dar certo, o `guess` deve satisfazer a condição `dia_que_descates_nasceu - guess = 1593`, portanto `guess=3`

Portanto, o input correto é:
`{"guess":3, "birth_year_minus_the_guess": 1593}`

## Como cheguei no resultado?

- Analisando o dapp, percebi que:
   - O payload do advance deve ser um json, com as chaves `guess` e `birth_year_minus_the_guess`
   - A função que decide se a input é válida estava já compilada, em binário
   - Caso o payload do advance esteja correto, o dapp envia um [notice](https://docs.cartesi.io/cartesi-rollups/1.3/rollups-apis/backend/notices/) para o nó Cartesi

### Como Resolvi

O primeiro passo foi tentar entender o que essa função já compilada faz. Tentei copiar o binário e descompilar no meu computador com a biblioteca `uncompyle6`, mas só dava erro. Aí lembrei que a Cartesi Machine roda na arquitetura RISC-V, portanto esse código compilado tem instruções que não são compativeis com meu computador x86.

Ao invés de subir uma VM RISC-V para tentar fazer a desassemblagem, utilizei o próprio Dapp para transformar o bytecode em mnemonics de RISC-V e printar elas no terminal.

Para os curiosos, coloquei esse Assembly no arquivo [`function.asm`](function.asm).

Utilizei um descompilador online e a função python é:
```python
def claim(guess, birth_year_minus_the_guess):
    a = 65535
    b = 489  # (2**16 >> 7) - 0x17
    
    # Loop para calcular o GCD usando o método de subtração
    while a != b:
        if a > b:
            a -= b
        else:
            b -= a
    
    # Verificação final
    if a == guess and birth_year_minus_the_guess == 1593:
        return True
    else:
        print("Error calculating GCD of a = 65535 and b = (2**16 >> 7) - 0x17.")
        return False
```

Sabendo de tudo isso, fica fácil!

Com o dapp rodando, utilizei o `Cartesi send generic` para enviar um [advance](https://docs.cartesi.io/cartesi-rollups/1.3/rollups-apis/backend/introduction/) com o payload correto.

Acessando o explorer do nó cartesi, conseguimos ver o notice que foi enviado como resposta para nosso advance, e, conectando o endpoint do GraphQL ao explorer, temos finalmente acesso à mensagem de sucesso!
