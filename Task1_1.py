import re


'''
Необходимо написать 3 класса для экранирования следующих данных на ruby или python без использования сторонних библиотек или сервисов:
1. Электронная почта. 
Экранировать нужно название почтового ящика, не домен.
Возможно указать следующие параметры при инициализации класса:
  а. Символ для экранирования, например "x" (aaa@aaa.com -> xxx@aaa.com)
Обязательно соблюдение количества символов для экранирования, то есть при aaaa@aaa.com должно получиться xxxx@aaa.com, а не xxx@aaa.com
2. Номер телефона. 
Экранировать нужно последние n символов, ОБЯЗАТЕЛЬНО сохранение пробелов в этом случае. Возможно указать следующие параметры при инициализации класса:
  а. Символ для экранирования, например "x" (+7 666 777 888 -> +7 666 777 xxx);
  б. Количество символов для экранирования (по умолчанию - 3)
Пробелы должны быть сохранены в оригинале, но при выводе должны сокращаться до одного. То есть, при запросе на экранирование с номером телефона "+7 666 777       888" и при выборе длины экранирования в 5 символов, должно выводиться "+7 666 7xx xxx"
3. Skype.
Обрабатывать нужно как обычные строки "skype:alex.max", так и ссылки, вроде "<a href=\"skype:alex.max?call\">skype</a>".
Результат в первом случае должен получиться "skype:xxx", а во втором - "<a href=\"skype:xxx?call\">skype</a>".
В данном случае не нужно учитывать длину экранируемой строки.
'''


class EmailMasker:
    def __init__(self, email: str, mask_symbol: str = 'x'):
        self.email = email
        self.mask_symbol = mask_symbol

    def get_masked_email(self) -> str:
        name, domain = self.email.split('@')
        masked_email = self.mask_symbol * len(name) + '@' + domain
        return masked_email


class PhoneMasker:
    def __init__(
            self,
            phone_number: str,
            mask_symbol: str = 'x',
            mask_len: int = 3
    ):
        self.phone_number = phone_number
        self.mask_symbol = mask_symbol
        self.mask_len = mask_len

    def get_masked_phone(self) -> str:
        phone_parts = re.split(r"\s+", self.phone_number.strip())
        normalized_phone = ' '.join(phone_parts)
        count_masked_symb = 0
        masked_phone = ''
        for i in range(len(normalized_phone) - 1, -1, -1):
            if count_masked_symb == self.mask_len:
                masked_phone = normalized_phone[:i + 1] + masked_phone[::-1]
                break
            else:
                if normalized_phone[i] == ' ':
                    masked_phone += normalized_phone[i]
                else:
                    masked_phone += self.mask_symbol
                    count_masked_symb += 1
        return masked_phone


class SkypeMasker:
    def __init__(self, skype_url: str, mask_symbol: str = 'x'):
        self.skype_url = skype_url
        self.mask_symbol = mask_symbol

    def get_masked_skype(self):
        if "skype:" in self.skype_url:
            masked_id = "skype:" + self.mask_symbol * 3
            return re.sub(r'(skype:[^?\"]+)', masked_id, self.skype_url)
        return self.skype_url


email = EmailMasker("testuser@example.com")
print(email.get_masked_email())

phone = PhoneMasker("+7 988    102    36 23")
print(phone.get_masked_phone())


skype1 = SkypeMasker("skype:alex.max")
print(skype1.get_masked_skype())

skype2 = SkypeMasker('<a href="skype:alex.max?call">skype</a>')
print(skype2.get_masked_skype())
