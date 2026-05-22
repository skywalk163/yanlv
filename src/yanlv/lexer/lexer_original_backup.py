"""
瑷€寰嬭瑷€璇嶆硶鍒嗘瀽鍣ㄥ疄鐜?
鏀寔jieba鍜孴HULAC涓ょ涓枃鍒嗚瘝鍣紝瀹炵幇鍏冩暟椹卞姩瑙ｆ瀽
"""

import re
import jieba
from typing import List, Iterator, Optional, Tuple, Literal
from .token import Token, TokenType
from .verb_categories import VERB_ARITY, get_verb_category, get_verb_arity


class YanLuLexer:
    """瑷€寰嬭瑷€璇嶆硶鍒嗘瀽鍣?""
    
    def __init__(self, segmenter: Literal["jieba", "thulac"] = "jieba"):
        """
        鍒濆鍖栬瘝娉曞垎鏋愬櫒
        
        Args:
            segmenter: 鍒嗚瘝鍣ㄧ被鍨嬶紝鍙€?"jieba" 鎴?"thulac"
        """
        self.segmenter_type = segmenter
        self.segmenter = None
        self._init_segmenter()
        # 涓枃鏍囩偣绗﹀彿
        self.chinese_punctuation = {
            '銆?: TokenType.PERIOD,
            '锛?: TokenType.COMMA,
            '锛?: TokenType.SEMICOLON,
            '锛?: TokenType.COLON,
            '銆?: TokenType.ENUMERATION,
            '锛?: TokenType.EXCLAMATION,
            '锛?: TokenType.QUESTION,
            '銆?: TokenType.BOOK_TITLE,
            '銆?: TokenType.BOOK_TITLE,
            '鈥︹€?: TokenType.ELLIPSIS,
            '鈥斺€?: TokenType.DASH,
            '锝?: TokenType.TILDE,
            '路': TokenType.MIDDLE_DOT,
            '銆?: TokenType.SQUARE_BRACKETS,
            '銆?: TokenType.SQUARE_BRACKETS,
        }
        
        # 涓枃鏁板瓧
        self.chinese_numbers = {
            '闆?: 0, '銆?: 0, '涓€': 1, '浜?: 2, '涓?: 3, '鍥?: 4,
            '浜?: 5, '鍏?: 6, '涓?: 7, '鍏?: 8, '涔?: 9,
            '鍗?: 10, '鐧?: 100, '鍗?: 1000, '涓?: 10000,
            '浜?: 100000000,
        }
        
        # 鍏抽敭璇?        self.keywords = {
            '濡傛灉': TokenType.IF,
            '瑕佹槸': TokenType.IF,
            '鍚﹀垯': TokenType.ELSE,
            '涓嶇劧': TokenType.ELSE,
            '褰?: TokenType.WHEN,
            '灏?: TokenType.THEN,
            '瀵逛簬': TokenType.FOR,
            '鍦?: TokenType.IN,
            '涓€鐩?: TokenType.WHILE,
            '瀹?: TokenType.DEF,
            '瀹氫箟': TokenType.DEF,
            '璁?: TokenType.SET,
            '鏄?: TokenType.IS,
            '绛変簬': TokenType.IS,
            '杩斿洖': TokenType.RETURN,
            '瀵煎叆': TokenType.IMPORT,
            '浠?: TokenType.FROM,
            '瀵煎嚭': TokenType.EXPORT,
        }
        
        # 鐘舵€佸叧閿瘝
        self.state_keywords = {
            '鍒濆鐘舵€?: TokenType.INITIAL_STATE,
            '鐘舵€佸彉涓?: TokenType.STATE_CHANGE,
            '鐘舵€佺炕杞?: TokenType.STATE_FLIP,
            '鐘舵€佷负': TokenType.STATE_IS,
        }
        
        # 鎰熺煡鍏抽敭璇?        self.perception_keywords = {
            '鐪嬪埌': TokenType.SEE,
            '鍙戠幇': TokenType.SEE,
            '妫€娴嬪埌': TokenType.SEE,
            '绔嬪埢': TokenType.IMMEDIATELY,
            '椹笂': TokenType.IMMEDIATELY,
            '绔嬪嵆': TokenType.IMMEDIATELY,
        }
        
        # 鏃堕棿鍏抽敭璇?        self.time_keywords = {
            '姣忛殧': TokenType.EVERY,
            '姣?: TokenType.EVERY,
            '浠ュ悗': TokenType.AFTER,
            '涔嬪悗': TokenType.AFTER,
        }
        
        # 杩愮畻绗?        self.operators = {
            '+': TokenType.PLUS,
            '-': TokenType.MINUS,
            '*': TokenType.MULTIPLY,
            '/': TokenType.DIVIDE,
            '%': TokenType.MODULO,
            '^': TokenType.POWER,
            '=': TokenType.EQUAL,
            '鈮?: TokenType.NOT_EQUAL,
            '<': TokenType.LESS,
            '>': TokenType.GREATER,
            '鈮?: TokenType.LESS_EQUAL,
            '鈮?: TokenType.GREATER_EQUAL,
            '涓?: TokenType.AND,
            '鎴?: TokenType.OR,
            '卢': TokenType.NOT,
        }
        
        # 鍒嗙粍绗﹀彿
        self.grouping_symbols = {
            '(': TokenType.LPAREN,
            ')': TokenType.RPAREN,
            '[': TokenType.LBRACKET,
            ']': TokenType.RBRACKET,
            '{': TokenType.LBRACE,
            '}': TokenType.RBRACE,
        }
        
        # 澶氳瑷€浠ｇ爜鍧楁爣璁?        self.code_block_markers = {
            '{{': TokenType.CODE_BLOCK_START,
            '}}': TokenType.CODE_BLOCK_END,
        }
        
        # 鐧惧濮擄紙鍓?0涓級
        self.bai_jia_xing = {
            '璧?, '閽?, '瀛?, '鏉?, '鍛?, '鍚?, '閮?, '鐜?, '鍐?, '闄?,
            '瑜?, '鍗?, '钂?, '娌?, '闊?, '鏉?, '鏈?, '绉?, '灏?, '璁?
        }
        
        # 鍐茬獊濮撴皬锛堜笉鑳戒綔涓哄彉閲忓悕锛?        self.conflict_surnames = {'绌?, '瑷€', '鍗?}
        
        self.number_pattern = re.compile(r'^\d+(\.\d+)?$')
        self.identifier_pattern = re.compile(r'^[\u4e00-\u9fffA-Za-z_][\u4e00-\u9fffA-Za-z0-9_]*$')
        
        Args:
            source_code: 婧愪唬鐮佸瓧绗︿覆
            
        Returns:
            璇嶆硶鍗曞厓鍒楄〃
        """
        tokens = []
        self.identifier_pattern = re.compile(r'^[\u4e00-\u9fffA-Za-z_][\u4e00-\u9fffA-Za-z0-9_]*$')
        lines = source_code.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            line_tokens = self._tokenize_line(line, line_num)
            tokens.extend(line_tokens)
            
            # 娣诲姞鎹㈣绗︼紙闄ら潪鏄渶鍚庝竴琛岋級
            if line_num < len(lines):
                tokens.append(Token(TokenType.NEWLINE, '\n', line_num, len(line) + 1, '\n'))
        
        # 娣诲姞鏂囦欢缁撴潫鏍囪
        tokens.append(Token(TokenType.EOF, '', len(lines) + 1, 1, ''))
        
        return tokens
    
    def _tokenize_line(self, line: str, line_num: int) -> List[Token]:
        """灏嗕竴琛屼唬鐮佽浆鎹负璇嶆硶鍗曞厓鍒楄〃"""
        tokens = []
        position = 0
        column = 1
        
        # 浣跨敤鍒嗚瘝鍣ㄨ繘琛屼腑鏂囧垎璇?        segments = self._segment(line)
        segment_index = 0
        
        while position < len(line):
            # 璺宠繃绌虹櫧瀛楃
            if line[position].isspace():
                if line[position] == '\n':
                    tokens.append(Token(TokenType.NEWLINE, '\n', line_num, column, '\n'))
                position += 1
                column += 1
                continue
            
            # 澶勭悊娉ㄩ噴
            if line[position] == '#':
                # 鍗曡娉ㄩ噴锛岃烦杩囨暣琛?                comment = line[position:]
                tokens.append(Token(TokenType.COMMENT, comment, line_num, column, comment))
                break
            
            # 澶勭悊澶氳瑷€浠ｇ爜鍧?            if line[position:position+2] == '{{':
                tokens.append(Token(TokenType.CODE_BLOCK_START, '{{', line_num, column, '{{'))
                position += 2
                column += 2
                continue
            
            if line[position:position+2] == '}}':
                tokens.append(Token(TokenType.CODE_BLOCK_END, '}}', line_num, column, '}}'))
                position += 2
                column += 2
                continue
            
            # 澶勭悊涓枃鏍囩偣绗﹀彿
            if line[position] in self.chinese_punctuation:
                char = line[position]
                token_type = self.chinese_punctuation[char]
                
                # 澶勭悊鎴愬鏍囩偣绗﹀彿
                if char in ('銆?, '銆?):
                    # 鏌ユ壘鍖归厤鐨勭粨鏉熺鍙?                    end_pos = line.find('銆? if char == '銆? else '銆?, position + 1)
                    if end_pos != -1:
                        value = line[position:end_pos + 1]
                        tokens.append(Token(token_type, value, line_num, column, value))
                        position = end_pos + 1
                        column += len(value)
                        continue
                
                tokens.append(Token(token_type, char, line_num, column, char))
                position += 1
                column += 1
                continue
            
            # 澶勭悊鐪佺暐鍙?            if line[position:position+2] == '鈥︹€?:
                tokens.append(Token(TokenType.ELLIPSIS, '鈥︹€?, line_num, column, '鈥︹€?))
                position += 2
                column += 2
                continue
            
            # 澶勭悊鐮存姌鍙?            if line[position:position+2] == '鈥斺€?:
                tokens.append(Token(TokenType.DASH, '鈥斺€?, line_num, column, '鈥斺€?))
                position += 2
                column += 2
                continue
            
            # 澶勭悊鍦嗗湀鍙?            if line[position] in '鈶犫憽鈶⑩懀鈶も懃鈶︹懅鈶ㄢ懇':
                tokens.append(Token(TokenType.CIRCLED_NUMBERS, line[position], line_num, column, line[position]))
                position += 1
                column += 1
                continue
            
            # 澶勭悊杩愮畻绗?            if line[position] in self.operators:
                # 妫€鏌ュ弻瀛楃杩愮畻绗?                if position + 1 < len(line):
                    two_char = line[position:position+2]
                    if two_char in ('鈮?, '鈮?, '鈮?):
                        tokens.append(Token(self.operators[two_char], two_char, line_num, column, two_char))
                        position += 2
                        column += 2
                        continue
                
                tokens.append(Token(self.operators[line[position]], line[position], line_num, column, line[position]))
                position += 1
                column += 1
                continue
            
            # 澶勭悊鍒嗙粍绗﹀彿
            if line[position] in self.grouping_symbols:
                tokens.append(Token(self.grouping_symbols[line[position]], line[position], line_num, column, line[position]))
                position += 1
                column += 1
                continue
            
            # 澶勭悊瀛楃涓插瓧闈㈤噺
            if line[position] in ('"', "'"):
                string_token = self._parse_string_literal(line, position, line_num, column)
                tokens.append(string_token)
                position += len(string_token.lexeme)
                column += len(string_token.lexeme)
                continue
            
            # 澶勭悊鏁板瓧瀛楅潰閲?            if line[position].isdigit() or (line[position] == '.' and position + 1 < len(line) and line[position + 1].isdigit()):
                number_token = self._parse_number(line, position, line_num, column)
                tokens.append(number_token)
                position += len(number_token.lexeme)
                column += len(number_token.lexeme)
                continue
            
            # 澶勭悊涓枃鏁板瓧
            if line[position] in self.chinese_numbers:
                chinese_number_token = self._parse_chinese_number(line, position, line_num, column)
                tokens.append(chinese_number_token)
                position += len(chinese_number_token.lexeme)
                column += len(chinese_number_token.lexeme)
                continue
            
            # 澶勭悊褰撳墠鍒嗚瘝娈?            if segment_index < len(segments):
                segment = segments[segment_index].strip()
                if segment:  # 璺宠繃绌哄垎璇?                    # 澶勭悊鍒嗚瘝娈?                    token = self._process_segment(segment, line_num, column)
                    tokens.append(token)
                    position += len(segment)
                    column += len(segment)
                segment_index += 1
            else:
                # 濡傛灉娌℃湁鏇村鍒嗚瘝锛屽鐞嗗墿浣欏瓧绗?                identifier_token = self._parse_identifier(line, position, line_num, column)
                tokens.append(identifier_token)
                position += len(identifier_token.lexeme)
                column += len(identifier_token.lexeme)
        
        return tokens
    
    def _process_segment(self, segment: str, line_num: int, column: int) -> Token:
        """澶勭悊鍒嗚瘝娈?""
        # 妫€鏌ユ槸鍚︿负鍏抽敭璇?        token_type = self._get_keyword_type(segment)
        if token_type:
            return Token(token_type, segment, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负鐧惧濮撳彉閲?        if self._is_bai_jia_xing(segment):
            return Token(TokenType.BAIJIAXING, segment, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负鍔ㄨ瘝
        arity = get_verb_arity(segment)
        if arity != 0:
            # 鏍规嵁鍏冩暟纭畾鍔ㄨ瘝绫诲瀷
            if arity == -1:
                token_type = TokenType.VERB_VAR
            elif arity == 0:
                token_type = TokenType.VERB_0
            elif arity == 1:
                token_type = TokenType.VERB_1
            elif arity == 2:
                token_type = TokenType.VERB_2
            elif arity == 3:
                token_type = TokenType.VERB_3
            else:
                token_type = TokenType.VERB_VAR
            
            return Token(token_type, segment, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负甯冨皵瀛楅潰閲?        if segment in ('鐪?, '鍋?, 'true', 'false', 'True', 'False'):
            value = segment in ('鐪?, 'true', 'True')
            return Token(TokenType.BOOLEAN, value, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负绌哄€?        if segment == '绌?:
            return Token(TokenType.NULL, None, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负鏁板瓧
        if segment.isdigit() or (segment.replace('.', '', 1).isdigit() and segment.count('.') == 1):
            try:
                if '.' in segment:
                    value = float(segment)
                else:
                    value = int(segment)
                return Token(TokenType.NUMBER, value, line_num, column, segment)
            except ValueError:
                pass
        
        # 妫€鏌ユ槸鍚︿负涓枃鏁板瓧
        if all(c in self.chinese_numbers for c in segment):
            value = self._chinese_to_arabic(segment)
            return Token(TokenType.CHINESE_NUMBER, value, line_num, column, segment)
        
        # 鏅€氭爣璇嗙
        return Token(TokenType.IDENTIFIER, segment, line_num, column, segment)
    
    def _parse_string_literal(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽瀛楃涓插瓧闈㈤噺"""
        quote_char = line[start]
        position = start + 1
        value = ''
        
        while position < len(line):
            char = line[position]
            
            if char == quote_char:
                # 缁撴潫寮曞彿
                position += 1
                break
            elif char == '\\' and position + 1 < len(line):
                # 杞箟瀛楃
                next_char = line[position + 1]
                if next_char in ('n', 't', '\\', '"', "'"):
                    value += self._escape_char(next_char)
                    position += 2
                else:
                    value += char
                    position += 1
            else:
                value += char
                position += 1
        
        lexeme = line[start:position]
        return Token(TokenType.STRING, value, line_num, column, lexeme)
    
    def _escape_char(self, char: str) -> str:
        """杞箟瀛楃"""
        escape_map = {
            'n': '\n',
            't': '\t',
            '\\': '\\',
            '"': '"',
            "'": "'",
        }
        return escape_map.get(char, char)
    
    def _parse_number(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽鏁板瓧瀛楅潰閲?""
        position = start
        
        # 瑙ｆ瀽鏁存暟閮ㄥ垎
        while position < len(line) and line[position].isdigit():
            position += 1
        
        # 瑙ｆ瀽灏忔暟閮ㄥ垎
        if position < len(line) and line[position] == '.':
            position += 1
            while position < len(line) and line[position].isdigit():
                position += 1
        
        # 瑙ｆ瀽绉戝璁℃暟娉?        if position < len(line) and line[position].lower() == 'e':
            position += 1
            if position < len(line) and line[position] in ('+', '-'):
                position += 1
            while position < len(line) and line[position].isdigit():
                position += 1
        
        lexeme = line[start:position]
        
        # 灏濊瘯杞崲涓烘暟瀛?        try:
            if '.' in lexeme or 'e' in lexeme.lower():
                value = float(lexeme)
            else:
                value = int(lexeme)
        except ValueError:
            value = lexeme  # 淇濇寔鍘熸牱
        
        return Token(TokenType.NUMBER, value, line_num, column, lexeme)
    
    def _parse_chinese_number(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽涓枃鏁板瓧"""
        position = start
        lexeme = ''
        
        while position < len(line) and line[position] in self.chinese_numbers:
            lexeme += line[position]
            position += 1
        
        # 杞崲涓洪樋鎷変集鏁板瓧
        value = self._chinese_to_arabic(lexeme)
        
        return Token(TokenType.CHINESE_NUMBER, value, line_num, column, lexeme)
    
    def _chinese_to_arabic(self, chinese_num: str) -> int:
        """灏嗕腑鏂囨暟瀛楄浆鎹负闃挎媺浼暟瀛?""
        if not chinese_num:
            return 0
        
        # 绠€鍗曞疄鐜帮紝鍙鐞嗗熀鏈暟瀛?        total = 0
        current = 0
        
        for char in chinese_num:
            num = self.chinese_numbers.get(char, 0)
            
            if num < 10:
                current = num
            elif num >= 10:
                if current == 0:
                    current = 1
                total += current * num
                current = 0
        
        total += current
        return total
    
    def _parse_identifier(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽鏍囪瘑绗?""
        position = start
        
        # 鏀堕泦鏍囪瘑绗﹀瓧绗?        while position < len(line) and self._is_identifier_char(line[position]):
            position += 1
        
        lexeme = line[start:position]
        
        # 妫€鏌ユ槸鍚︿负鍏抽敭璇?        token_type = self._get_keyword_type(lexeme)
        if token_type:
            return Token(token_type, lexeme, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负鐧惧濮撳彉閲?        if self._is_bai_jia_xing(lexeme):
            return Token(TokenType.BAIJIAXING, lexeme, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负鍔ㄨ瘝
        arity = get_verb_arity(lexeme)
        if arity != 0:
            # 鏍规嵁鍏冩暟纭畾鍔ㄨ瘝绫诲瀷
            if arity == -1:
                token_type = TokenType.VERB_VAR
            elif arity == 0:
                token_type = TokenType.VERB_0
            elif arity == 1:
                token_type = TokenType.VERB_1
            elif arity == 2:
                token_type = TokenType.VERB_2
            elif arity == 3:
                token_type = TokenType.VERB_3
            else:
                token_type = TokenType.VERB_VAR
            
            return Token(token_type, lexeme, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负甯冨皵瀛楅潰閲?        if lexeme in ('鐪?, '鍋?, 'true', 'false', 'True', 'False'):
            value = lexeme in ('鐪?, 'true', 'True')
            return Token(TokenType.BOOLEAN, value, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负绌哄€?        if lexeme == '绌?:
            return Token(TokenType.NULL, None, line_num, column, lexeme)
        
        # 灏濊瘯涓枃鍒嗚瘝
        if len(lexeme) > 1 and any('\u4e00' <= c <= '\u9fff' for c in lexeme):
            # 浣跨敤jieba杩涜涓枃鍒嗚瘝
            segments = self._segment(lexeme)
            if len(segments) > 1:
                # 濡傛灉鏄涓瘝锛岃繑鍥炵涓€涓瘝浣滀负鏍囪瘑绗?                first_segment = segments[0]
                # 閫掑綊澶勭悊绗竴涓瘝
                return self._parse_identifier(first_segment, 0, line_num, column)
        
        # 鏅€氭爣璇嗙
        return Token(TokenType.IDENTIFIER, lexeme, line_num, column, lexeme)
    
    def _is_identifier_char(self, char: str) -> bool:
        """妫€鏌ュ瓧绗︽槸鍚︿负鏍囪瘑绗﹀瓧绗?""
        # 涓枃瀛楃銆佽嫳鏂囧瓧姣嶃€佹暟瀛椼€佷笅鍒掔嚎
        return ('\u4e00' <= char <= '\u9fff' or
                'a' <= char <= 'z' or
                'A' <= char <= 'Z' or
                char.isdigit() or
                char == '_')
    
    def _get_keyword_type(self, lexeme: str) -> Optional[TokenType]:
        """鑾峰彇鍏抽敭璇嶇被鍨?""
        # 妫€鏌ョ姸鎬佸叧閿瘝锛堝瀛楋級
        for keyword, token_type in self.state_keywords.items():
            if lexeme.startswith(keyword):
                return token_type
        
        # 妫€鏌ユ劅鐭ュ叧閿瘝锛堝瀛楋級
        for keyword, token_type in self.perception_keywords.items():
            if lexeme.startswith(keyword):
                return token_type
        
        # 妫€鏌ユ椂闂村叧閿瘝锛堝瀛楋級
        for keyword, token_type in self.time_keywords.items():
            if lexeme.startswith(keyword):
                return token_type
        
        # 妫€鏌ユ櫘閫氬叧閿瘝
        return self.keywords.get(lexeme)
    
    def _is_bai_jia_xing(self, lexeme: str) -> bool:
        """妫€鏌ユ槸鍚︿负鐧惧濮撳彉閲?""
        if not lexeme:
            return False
        
        # 鑾峰彇濮撴皬锛堢涓€涓瓧绗︼級
        surname = lexeme[0]
        
        # 妫€鏌ユ槸鍚︿负鍐茬獊濮撴皬
        if surname in self.conflict_surnames:
            return False
        
        # 妫€鏌ユ槸鍚︿负鐧惧濮?        return surname in self.bai_jia_xing
    
    def print_tokens(self, tokens: List[Token]) -> None:
        """鎵撳嵃璇嶆硶鍗曞厓鍒楄〃"""
        print("璇嶆硶鍒嗘瀽缁撴灉:")
        print("=" * 80)
        print(f"{'琛?:<4} {'鍒?:<4} {'绫诲瀷':<20} {'鍊?:<20} {'璇嶇礌':<20}")
        print("-" * 80)
        
        for token in tokens:
            value_str = str(token.value)
            if len(value_str) > 18:
                value_str = value_str[:15] + "..."
            
            lexeme_str = token.lexeme
            if len(lexeme_str) > 18:
                lexeme_str = lexeme_str[:15] + "..."
            
            print(f"{token.line:<4} {token.column:<4} {token.type.value:<20} {value_str:<20} {lexeme_str:<20}")
        
        print("=" * 80)


# 娴嬭瘯鍑芥暟
def test_lexer():
    """娴嬭瘯璇嶆硶鍒嗘瀽鍣?""
    print("璇嶆硶鍒嗘瀽鍣ㄦ祴璇?)
    print("=" * 50)
    
    lexer = YanLuLexer()
    
    # 娴嬭瘯鐢ㄤ緥
    test_cases = [
        (
            "瀹氭俯搴︽槸25銆?,
            "鍙橀噺瀹氫箟"
        ),
        (
            "濡傛灉娓╁害澶?0灏卞紑鍚鎵囥€?,
            "鏉′欢璇彞"
        ),
        (
            "瀵逛簬i鍦?鍒?0锛氬嵃i銆?,
            "寰幆璇彞"
        ),
        (
            "娓╁害鍙樹负30搴︺€?,
            "鐘舵€佽浆鎹?
        ),
        (
            "寮犱笁銆佹潕鍥涳紝璁＄畻鎶樻墸銆?,
            "鎰忓悎寮忓嚱鏁拌皟鐢?
        ),
        (
            "'浣犲ソ锛屼笘鐣?",
            "瀛楃涓插瓧闈㈤噺"
        ),
        (
            "鐪熶笖鍋?,
            "甯冨皵杩愮畻"
        ),
        (
            "瀹歺绛変簬鍗佸姞浜斻€?,
            "涓枃鏁板瓧"
        ),
    ]
    
    for source_code, description in test_cases:
        print(f"\n娴嬭瘯: {description}")
        print(f"婧愪唬鐮? {source_code}")
        
        try:
            tokens = lexer.tokenize(source_code)
            lexer.print_tokens(tokens)
        except Exception as e:
            print(f"閿欒: {e}")
    
    print("=" * 50)
    print("娴嬭瘯瀹屾垚")


if __name__ == "__main__":
    test_lexer())
        self.identifier_pattern = re.compile(r'^[\u4e00-\u9fffA-Za-z_][\u4e00-\u9fffA-Za-z0-9_]*
        """
        灏嗘簮浠ｇ爜杞崲涓鸿瘝娉曞崟鍏冨垪琛?        
        Args:
            source_code: 婧愪唬鐮佸瓧绗︿覆
            
        Returns:
            璇嶆硶鍗曞厓鍒楄〃
        """
        tokens = []
        lines = source_code.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            line_tokens = self._tokenize_line(line, line_num)
            tokens.extend(line_tokens)
            
            # 娣诲姞鎹㈣绗︼紙闄ら潪鏄渶鍚庝竴琛岋級
            if line_num < len(lines):
                tokens.append(Token(TokenType.NEWLINE, '\n', line_num, len(line) + 1, '\n'))
        
        # 娣诲姞鏂囦欢缁撴潫鏍囪
        tokens.append(Token(TokenType.EOF, '', len(lines) + 1, 1, ''))
        
        return tokens
    
    def _tokenize_line(self, line: str, line_num: int) -> List[Token]:
        """灏嗕竴琛屼唬鐮佽浆鎹负璇嶆硶鍗曞厓鍒楄〃"""
        tokens = []
        position = 0
        column = 1
        
        # 浣跨敤鍒嗚瘝鍣ㄨ繘琛屼腑鏂囧垎璇?        segments = self._segment(line)
        segment_index = 0
        
        while position < len(line):
            # 璺宠繃绌虹櫧瀛楃
            if line[position].isspace():
                if line[position] == '\n':
                    tokens.append(Token(TokenType.NEWLINE, '\n', line_num, column, '\n'))
                position += 1
                column += 1
                continue
            
            # 澶勭悊娉ㄩ噴
            if line[position] == '#':
                # 鍗曡娉ㄩ噴锛岃烦杩囨暣琛?                comment = line[position:]
                tokens.append(Token(TokenType.COMMENT, comment, line_num, column, comment))
                break
            
            # 澶勭悊澶氳瑷€浠ｇ爜鍧?            if line[position:position+2] == '{{':
                tokens.append(Token(TokenType.CODE_BLOCK_START, '{{', line_num, column, '{{'))
                position += 2
                column += 2
                continue
            
            if line[position:position+2] == '}}':
                tokens.append(Token(TokenType.CODE_BLOCK_END, '}}', line_num, column, '}}'))
                position += 2
                column += 2
                continue
            
            # 澶勭悊涓枃鏍囩偣绗﹀彿
            if line[position] in self.chinese_punctuation:
                char = line[position]
                token_type = self.chinese_punctuation[char]
                
                # 澶勭悊鎴愬鏍囩偣绗﹀彿
                if char in ('銆?, '銆?):
                    # 鏌ユ壘鍖归厤鐨勭粨鏉熺鍙?                    end_pos = line.find('銆? if char == '銆? else '銆?, position + 1)
                    if end_pos != -1:
                        value = line[position:end_pos + 1]
                        tokens.append(Token(token_type, value, line_num, column, value))
                        position = end_pos + 1
                        column += len(value)
                        continue
                
                tokens.append(Token(token_type, char, line_num, column, char))
                position += 1
                column += 1
                continue
            
            # 澶勭悊鐪佺暐鍙?            if line[position:position+2] == '鈥︹€?:
                tokens.append(Token(TokenType.ELLIPSIS, '鈥︹€?, line_num, column, '鈥︹€?))
                position += 2
                column += 2
                continue
            
            # 澶勭悊鐮存姌鍙?            if line[position:position+2] == '鈥斺€?:
                tokens.append(Token(TokenType.DASH, '鈥斺€?, line_num, column, '鈥斺€?))
                position += 2
                column += 2
                continue
            
            # 澶勭悊鍦嗗湀鍙?            if line[position] in '鈶犫憽鈶⑩懀鈶も懃鈶︹懅鈶ㄢ懇':
                tokens.append(Token(TokenType.CIRCLED_NUMBERS, line[position], line_num, column, line[position]))
                position += 1
                column += 1
                continue
            
            # 澶勭悊杩愮畻绗?            if line[position] in self.operators:
                # 妫€鏌ュ弻瀛楃杩愮畻绗?                if position + 1 < len(line):
                    two_char = line[position:position+2]
                    if two_char in ('鈮?, '鈮?, '鈮?):
                        tokens.append(Token(self.operators[two_char], two_char, line_num, column, two_char))
                        position += 2
                        column += 2
                        continue
                
                tokens.append(Token(self.operators[line[position]], line[position], line_num, column, line[position]))
                position += 1
                column += 1
                continue
            
            # 澶勭悊鍒嗙粍绗﹀彿
            if line[position] in self.grouping_symbols:
                tokens.append(Token(self.grouping_symbols[line[position]], line[position], line_num, column, line[position]))
                position += 1
                column += 1
                continue
            
            # 澶勭悊瀛楃涓插瓧闈㈤噺
            if line[position] in ('"', "'"):
                string_token = self._parse_string_literal(line, position, line_num, column)
                tokens.append(string_token)
                position += len(string_token.lexeme)
                column += len(string_token.lexeme)
                continue
            
            # 澶勭悊鏁板瓧瀛楅潰閲?            if line[position].isdigit() or (line[position] == '.' and position + 1 < len(line) and line[position + 1].isdigit()):
                number_token = self._parse_number(line, position, line_num, column)
                tokens.append(number_token)
                position += len(number_token.lexeme)
                column += len(number_token.lexeme)
                continue
            
            # 澶勭悊涓枃鏁板瓧
            if line[position] in self.chinese_numbers:
                chinese_number_token = self._parse_chinese_number(line, position, line_num, column)
                tokens.append(chinese_number_token)
                position += len(chinese_number_token.lexeme)
                column += len(chinese_number_token.lexeme)
                continue
            
            # 澶勭悊褰撳墠鍒嗚瘝娈?            if segment_index < len(segments):
                segment = segments[segment_index].strip()
                if segment:  # 璺宠繃绌哄垎璇?                    # 澶勭悊鍒嗚瘝娈?                    token = self._process_segment(segment, line_num, column)
                    tokens.append(token)
                    position += len(segment)
                    column += len(segment)
                segment_index += 1
            else:
                # 濡傛灉娌℃湁鏇村鍒嗚瘝锛屽鐞嗗墿浣欏瓧绗?                identifier_token = self._parse_identifier(line, position, line_num, column)
                tokens.append(identifier_token)
                position += len(identifier_token.lexeme)
                column += len(identifier_token.lexeme)
        
        return tokens
    
    def _process_segment(self, segment: str, line_num: int, column: int) -> Token:
        """澶勭悊鍒嗚瘝娈?""
        # 妫€鏌ユ槸鍚︿负鍏抽敭璇?        token_type = self._get_keyword_type(segment)
        if token_type:
            return Token(token_type, segment, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负鐧惧濮撳彉閲?        if self._is_bai_jia_xing(segment):
            return Token(TokenType.BAIJIAXING, segment, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负鍔ㄨ瘝
        arity = get_verb_arity(segment)
        if arity != 0:
            # 鏍规嵁鍏冩暟纭畾鍔ㄨ瘝绫诲瀷
            if arity == -1:
                token_type = TokenType.VERB_VAR
            elif arity == 0:
                token_type = TokenType.VERB_0
            elif arity == 1:
                token_type = TokenType.VERB_1
            elif arity == 2:
                token_type = TokenType.VERB_2
            elif arity == 3:
                token_type = TokenType.VERB_3
            else:
                token_type = TokenType.VERB_VAR
            
            return Token(token_type, segment, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负甯冨皵瀛楅潰閲?        if segment in ('鐪?, '鍋?, 'true', 'false', 'True', 'False'):
            value = segment in ('鐪?, 'true', 'True')
            return Token(TokenType.BOOLEAN, value, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负绌哄€?        if segment == '绌?:
            return Token(TokenType.NULL, None, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负鏁板瓧
        if segment.isdigit() or (segment.replace('.', '', 1).isdigit() and segment.count('.') == 1):
            try:
                if '.' in segment:
                    value = float(segment)
                else:
                    value = int(segment)
                return Token(TokenType.NUMBER, value, line_num, column, segment)
            except ValueError:
                pass
        
        # 妫€鏌ユ槸鍚︿负涓枃鏁板瓧
        if all(c in self.chinese_numbers for c in segment):
            value = self._chinese_to_arabic(segment)
            return Token(TokenType.CHINESE_NUMBER, value, line_num, column, segment)
        
        # 鏅€氭爣璇嗙
        return Token(TokenType.IDENTIFIER, segment, line_num, column, segment)
    
    def _parse_string_literal(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽瀛楃涓插瓧闈㈤噺"""
        quote_char = line[start]
        position = start + 1
        value = ''
        
        while position < len(line):
            char = line[position]
            
            if char == quote_char:
                # 缁撴潫寮曞彿
                position += 1
                break
            elif char == '\\' and position + 1 < len(line):
                # 杞箟瀛楃
                next_char = line[position + 1]
                if next_char in ('n', 't', '\\', '"', "'"):
                    value += self._escape_char(next_char)
                    position += 2
                else:
                    value += char
                    position += 1
            else:
                value += char
                position += 1
        
        lexeme = line[start:position]
        return Token(TokenType.STRING, value, line_num, column, lexeme)
    
    def _escape_char(self, char: str) -> str:
        """杞箟瀛楃"""
        escape_map = {
            'n': '\n',
            't': '\t',
            '\\': '\\',
            '"': '"',
            "'": "'",
        }
        return escape_map.get(char, char)
    
    def _parse_number(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽鏁板瓧瀛楅潰閲?""
        position = start
        
        # 瑙ｆ瀽鏁存暟閮ㄥ垎
        while position < len(line) and line[position].isdigit():
            position += 1
        
        # 瑙ｆ瀽灏忔暟閮ㄥ垎
        if position < len(line) and line[position] == '.':
            position += 1
            while position < len(line) and line[position].isdigit():
                position += 1
        
        # 瑙ｆ瀽绉戝璁℃暟娉?        if position < len(line) and line[position].lower() == 'e':
            position += 1
            if position < len(line) and line[position] in ('+', '-'):
                position += 1
            while position < len(line) and line[position].isdigit():
                position += 1
        
        lexeme = line[start:position]
        
        # 灏濊瘯杞崲涓烘暟瀛?        try:
            if '.' in lexeme or 'e' in lexeme.lower():
                value = float(lexeme)
            else:
                value = int(lexeme)
        except ValueError:
            value = lexeme  # 淇濇寔鍘熸牱
        
        return Token(TokenType.NUMBER, value, line_num, column, lexeme)
    
    def _parse_chinese_number(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽涓枃鏁板瓧"""
        position = start
        lexeme = ''
        
        while position < len(line) and line[position] in self.chinese_numbers:
            lexeme += line[position]
            position += 1
        
        # 杞崲涓洪樋鎷変集鏁板瓧
        value = self._chinese_to_arabic(lexeme)
        
        return Token(TokenType.CHINESE_NUMBER, value, line_num, column, lexeme)
    
    def _chinese_to_arabic(self, chinese_num: str) -> int:
        """灏嗕腑鏂囨暟瀛楄浆鎹负闃挎媺浼暟瀛?""
        if not chinese_num:
            return 0
        
        # 绠€鍗曞疄鐜帮紝鍙鐞嗗熀鏈暟瀛?        total = 0
        current = 0
        
        for char in chinese_num:
            num = self.chinese_numbers.get(char, 0)
            
            if num < 10:
                current = num
            elif num >= 10:
                if current == 0:
                    current = 1
                total += current * num
                current = 0
        
        total += current
        return total
    
    def _parse_identifier(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽鏍囪瘑绗?""
        position = start
        
        # 鏀堕泦鏍囪瘑绗﹀瓧绗?        while position < len(line) and self._is_identifier_char(line[position]):
            position += 1
        
        lexeme = line[start:position]
        
        # 妫€鏌ユ槸鍚︿负鍏抽敭璇?        token_type = self._get_keyword_type(lexeme)
        if token_type:
            return Token(token_type, lexeme, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负鐧惧濮撳彉閲?        if self._is_bai_jia_xing(lexeme):
            return Token(TokenType.BAIJIAXING, lexeme, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负鍔ㄨ瘝
        arity = get_verb_arity(lexeme)
        if arity != 0:
            # 鏍规嵁鍏冩暟纭畾鍔ㄨ瘝绫诲瀷
            if arity == -1:
                token_type = TokenType.VERB_VAR
            elif arity == 0:
                token_type = TokenType.VERB_0
            elif arity == 1:
                token_type = TokenType.VERB_1
            elif arity == 2:
                token_type = TokenType.VERB_2
            elif arity == 3:
                token_type = TokenType.VERB_3
            else:
                token_type = TokenType.VERB_VAR
            
            return Token(token_type, lexeme, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负甯冨皵瀛楅潰閲?        if lexeme in ('鐪?, '鍋?, 'true', 'false', 'True', 'False'):
            value = lexeme in ('鐪?, 'true', 'True')
            return Token(TokenType.BOOLEAN, value, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负绌哄€?        if lexeme == '绌?:
            return Token(TokenType.NULL, None, line_num, column, lexeme)
        
        # 灏濊瘯涓枃鍒嗚瘝
        if len(lexeme) > 1 and any('\u4e00' <= c <= '\u9fff' for c in lexeme):
            # 浣跨敤jieba杩涜涓枃鍒嗚瘝
            segments = self._segment(lexeme)
            if len(segments) > 1:
                # 濡傛灉鏄涓瘝锛岃繑鍥炵涓€涓瘝浣滀负鏍囪瘑绗?                first_segment = segments[0]
                # 閫掑綊澶勭悊绗竴涓瘝
                return self._parse_identifier(first_segment, 0, line_num, column)
        
        # 鏅€氭爣璇嗙
        return Token(TokenType.IDENTIFIER, lexeme, line_num, column, lexeme)
    
    def _is_identifier_char(self, char: str) -> bool:
        """妫€鏌ュ瓧绗︽槸鍚︿负鏍囪瘑绗﹀瓧绗?""
        # 涓枃瀛楃銆佽嫳鏂囧瓧姣嶃€佹暟瀛椼€佷笅鍒掔嚎
        return ('\u4e00' <= char <= '\u9fff' or
                'a' <= char <= 'z' or
                'A' <= char <= 'Z' or
                char.isdigit() or
                char == '_')
    
    def _get_keyword_type(self, lexeme: str) -> Optional[TokenType]:
        """鑾峰彇鍏抽敭璇嶇被鍨?""
        # 妫€鏌ョ姸鎬佸叧閿瘝锛堝瀛楋級
        for keyword, token_type in self.state_keywords.items():
            if lexeme.startswith(keyword):
                return token_type
        
        # 妫€鏌ユ劅鐭ュ叧閿瘝锛堝瀛楋級
        for keyword, token_type in self.perception_keywords.items():
            if lexeme.startswith(keyword):
                return token_type
        
        # 妫€鏌ユ椂闂村叧閿瘝锛堝瀛楋級
        for keyword, token_type in self.time_keywords.items():
            if lexeme.startswith(keyword):
                return token_type
        
        # 妫€鏌ユ櫘閫氬叧閿瘝
        return self.keywords.get(lexeme)
    
    def _is_bai_jia_xing(self, lexeme: str) -> bool:
        """妫€鏌ユ槸鍚︿负鐧惧濮撳彉閲?""
        if not lexeme:
            return False
        
        # 鑾峰彇濮撴皬锛堢涓€涓瓧绗︼級
        surname = lexeme[0]
        
        # 妫€鏌ユ槸鍚︿负鍐茬獊濮撴皬
        if surname in self.conflict_surnames:
            return False
        
        # 妫€鏌ユ槸鍚︿负鐧惧濮?        return surname in self.bai_jia_xing
    
    def print_tokens(self, tokens: List[Token]) -> None:
        """鎵撳嵃璇嶆硶鍗曞厓鍒楄〃"""
        print("璇嶆硶鍒嗘瀽缁撴灉:")
        print("=" * 80)
        print(f"{'琛?:<4} {'鍒?:<4} {'绫诲瀷':<20} {'鍊?:<20} {'璇嶇礌':<20}")
        print("-" * 80)
        
        for token in tokens:
            value_str = str(token.value)
            if len(value_str) > 18:
                value_str = value_str[:15] + "..."
            
            lexeme_str = token.lexeme
            if len(lexeme_str) > 18:
                lexeme_str = lexeme_str[:15] + "..."
            
            print(f"{token.line:<4} {token.column:<4} {token.type.value:<20} {value_str:<20} {lexeme_str:<20}")
        
        print("=" * 80)


# 娴嬭瘯鍑芥暟
def test_lexer():
    """娴嬭瘯璇嶆硶鍒嗘瀽鍣?""
    print("璇嶆硶鍒嗘瀽鍣ㄦ祴璇?)
    print("=" * 50)
    
    lexer = YanLuLexer()
    
    # 娴嬭瘯鐢ㄤ緥
    test_cases = [
        (
            "瀹氭俯搴︽槸25銆?,
            "鍙橀噺瀹氫箟"
        ),
        (
            "濡傛灉娓╁害澶?0灏卞紑鍚鎵囥€?,
            "鏉′欢璇彞"
        ),
        (
            "瀵逛簬i鍦?鍒?0锛氬嵃i銆?,
            "寰幆璇彞"
        ),
        (
            "娓╁害鍙樹负30搴︺€?,
            "鐘舵€佽浆鎹?
        ),
        (
            "寮犱笁銆佹潕鍥涳紝璁＄畻鎶樻墸銆?,
            "鎰忓悎寮忓嚱鏁拌皟鐢?
        ),
        (
            "'浣犲ソ锛屼笘鐣?",
            "瀛楃涓插瓧闈㈤噺"
        ),
        (
            "鐪熶笖鍋?,
            "甯冨皵杩愮畻"
        ),
        (
            "瀹歺绛変簬鍗佸姞浜斻€?,
            "涓枃鏁板瓧"
        ),
    ]
    
    for source_code, description in test_cases:
        print(f"\n娴嬭瘯: {description}")
        print(f"婧愪唬鐮? {source_code}")
        
        try:
            tokens = lexer.tokenize(source_code)
            lexer.print_tokens(tokens)
        except Exception as e:
            print(f"閿欒: {e}")
    
    print("=" * 50)
    print("娴嬭瘯瀹屾垚")


if __name__ == "__main__":
    test_lexer())
    
    def _init_segmenter(self):
        """鍒濆鍖栧垎璇嶅櫒"""
        if self.segmenter_type == "thulac":
            try:
                import thulac
                # 浣跨敤seg_only=True鍙繘琛屽垎璇嶏紝涓嶈繘琛岃瘝鎬ф爣娉?                self.segmenter = thulac.thulac(seg_only=True, model_path=None)
                print(f"浣跨敤THULAC鍒嗚瘝鍣?(seg_only妯″紡)")
            except ImportError:
                print("璀﹀憡: 鏈畨瑁匱HULAC锛屽洖閫€鍒癹ieba鍒嗚瘝鍣?)
                print("瀹夎鍛戒护: pip install thulac")
                self.segmenter_type = "jieba"
                self.segmenter = jieba
        else:
            # 榛樿浣跨敤jieba
            self.segmenter = jieba
            print(f"浣跨敤jieba鍒嗚瘝鍣?)
    
    def _segment(self, text: str) -> List[str]:
        """
        鍒嗚瘝鏂规硶
        
        Args:
            text: 寰呭垎璇嶇殑鏂囨湰
            
        Returns:
            鍒嗚瘝缁撴灉鍒楄〃
        """
        if self.segmenter_type == "thulac":
            # THULAC鍒嗚瘝
            result = self.segmenter.cut(text, text=True)
            return result.split()
        else:
            # jieba鍒嗚瘝
            return list(self.segmenter.lcut(text))
        
    def tokenize(self, source_code: str) -> List[Token]:
        """
        灏嗘簮浠ｇ爜杞崲涓鸿瘝娉曞崟鍏冨垪琛?        
        Args:
            source_code: 婧愪唬鐮佸瓧绗︿覆
            
        Returns:
            璇嶆硶鍗曞厓鍒楄〃
        """
        tokens = []
        lines = source_code.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            line_tokens = self._tokenize_line(line, line_num)
            tokens.extend(line_tokens)
            
            # 娣诲姞鎹㈣绗︼紙闄ら潪鏄渶鍚庝竴琛岋級
            if line_num < len(lines):
                tokens.append(Token(TokenType.NEWLINE, '\n', line_num, len(line) + 1, '\n'))
        
        # 娣诲姞鏂囦欢缁撴潫鏍囪
        tokens.append(Token(TokenType.EOF, '', len(lines) + 1, 1, ''))
        
        return tokens
    
    def _tokenize_line(self, line: str, line_num: int) -> List[Token]:
        """灏嗕竴琛屼唬鐮佽浆鎹负璇嶆硶鍗曞厓鍒楄〃"""
        tokens = []
        position = 0
        column = 1
        
        # 浣跨敤鍒嗚瘝鍣ㄨ繘琛屼腑鏂囧垎璇?        segments = self._segment(line)
        segment_index = 0
        
        while position < len(line):
            # 璺宠繃绌虹櫧瀛楃
            if line[position].isspace():
                if line[position] == '\n':
                    tokens.append(Token(TokenType.NEWLINE, '\n', line_num, column, '\n'))
                position += 1
                column += 1
                continue
            
            # 澶勭悊娉ㄩ噴
            if line[position] == '#':
                # 鍗曡娉ㄩ噴锛岃烦杩囨暣琛?                comment = line[position:]
                tokens.append(Token(TokenType.COMMENT, comment, line_num, column, comment))
                break
            
            # 澶勭悊澶氳瑷€浠ｇ爜鍧?            if line[position:position+2] == '{{':
                tokens.append(Token(TokenType.CODE_BLOCK_START, '{{', line_num, column, '{{'))
                position += 2
                column += 2
                continue
            
            if line[position:position+2] == '}}':
                tokens.append(Token(TokenType.CODE_BLOCK_END, '}}', line_num, column, '}}'))
                position += 2
                column += 2
                continue
            
            # 澶勭悊涓枃鏍囩偣绗﹀彿
            if line[position] in self.chinese_punctuation:
                char = line[position]
                token_type = self.chinese_punctuation[char]
                
                # 澶勭悊鎴愬鏍囩偣绗﹀彿
                if char in ('銆?, '銆?):
                    # 鏌ユ壘鍖归厤鐨勭粨鏉熺鍙?                    end_pos = line.find('銆? if char == '銆? else '銆?, position + 1)
                    if end_pos != -1:
                        value = line[position:end_pos + 1]
                        tokens.append(Token(token_type, value, line_num, column, value))
                        position = end_pos + 1
                        column += len(value)
                        continue
                
                tokens.append(Token(token_type, char, line_num, column, char))
                position += 1
                column += 1
                continue
            
            # 澶勭悊鐪佺暐鍙?            if line[position:position+2] == '鈥︹€?:
                tokens.append(Token(TokenType.ELLIPSIS, '鈥︹€?, line_num, column, '鈥︹€?))
                position += 2
                column += 2
                continue
            
            # 澶勭悊鐮存姌鍙?            if line[position:position+2] == '鈥斺€?:
                tokens.append(Token(TokenType.DASH, '鈥斺€?, line_num, column, '鈥斺€?))
                position += 2
                column += 2
                continue
            
            # 澶勭悊鍦嗗湀鍙?            if line[position] in '鈶犫憽鈶⑩懀鈶も懃鈶︹懅鈶ㄢ懇':
                tokens.append(Token(TokenType.CIRCLED_NUMBERS, line[position], line_num, column, line[position]))
                position += 1
                column += 1
                continue
            
            # 澶勭悊杩愮畻绗?            if line[position] in self.operators:
                # 妫€鏌ュ弻瀛楃杩愮畻绗?                if position + 1 < len(line):
                    two_char = line[position:position+2]
                    if two_char in ('鈮?, '鈮?, '鈮?):
                        tokens.append(Token(self.operators[two_char], two_char, line_num, column, two_char))
                        position += 2
                        column += 2
                        continue
                
                tokens.append(Token(self.operators[line[position]], line[position], line_num, column, line[position]))
                position += 1
                column += 1
                continue
            
            # 澶勭悊鍒嗙粍绗﹀彿
            if line[position] in self.grouping_symbols:
                tokens.append(Token(self.grouping_symbols[line[position]], line[position], line_num, column, line[position]))
                position += 1
                column += 1
                continue
            
            # 澶勭悊瀛楃涓插瓧闈㈤噺
            if line[position] in ('"', "'"):
                string_token = self._parse_string_literal(line, position, line_num, column)
                tokens.append(string_token)
                position += len(string_token.lexeme)
                column += len(string_token.lexeme)
                continue
            
            # 澶勭悊鏁板瓧瀛楅潰閲?            if line[position].isdigit() or (line[position] == '.' and position + 1 < len(line) and line[position + 1].isdigit()):
                number_token = self._parse_number(line, position, line_num, column)
                tokens.append(number_token)
                position += len(number_token.lexeme)
                column += len(number_token.lexeme)
                continue
            
            # 澶勭悊涓枃鏁板瓧
            if line[position] in self.chinese_numbers:
                chinese_number_token = self._parse_chinese_number(line, position, line_num, column)
                tokens.append(chinese_number_token)
                position += len(chinese_number_token.lexeme)
                column += len(chinese_number_token.lexeme)
                continue
            
            # 澶勭悊褰撳墠鍒嗚瘝娈?            if segment_index < len(segments):
                segment = segments[segment_index].strip()
                if segment:  # 璺宠繃绌哄垎璇?                    # 澶勭悊鍒嗚瘝娈?                    token = self._process_segment(segment, line_num, column)
                    tokens.append(token)
                    position += len(segment)
                    column += len(segment)
                segment_index += 1
            else:
                # 濡傛灉娌℃湁鏇村鍒嗚瘝锛屽鐞嗗墿浣欏瓧绗?                identifier_token = self._parse_identifier(line, position, line_num, column)
                tokens.append(identifier_token)
                position += len(identifier_token.lexeme)
                column += len(identifier_token.lexeme)
        
        return tokens
    
    def _process_segment(self, segment: str, line_num: int, column: int) -> Token:
        """澶勭悊鍒嗚瘝娈?""
        # 妫€鏌ユ槸鍚︿负鍏抽敭璇?        token_type = self._get_keyword_type(segment)
        if token_type:
            return Token(token_type, segment, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负鐧惧濮撳彉閲?        if self._is_bai_jia_xing(segment):
            return Token(TokenType.BAIJIAXING, segment, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负鍔ㄨ瘝
        arity = get_verb_arity(segment)
        if arity != 0:
            # 鏍规嵁鍏冩暟纭畾鍔ㄨ瘝绫诲瀷
            if arity == -1:
                token_type = TokenType.VERB_VAR
            elif arity == 0:
                token_type = TokenType.VERB_0
            elif arity == 1:
                token_type = TokenType.VERB_1
            elif arity == 2:
                token_type = TokenType.VERB_2
            elif arity == 3:
                token_type = TokenType.VERB_3
            else:
                token_type = TokenType.VERB_VAR
            
            return Token(token_type, segment, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负甯冨皵瀛楅潰閲?        if segment in ('鐪?, '鍋?, 'true', 'false', 'True', 'False'):
            value = segment in ('鐪?, 'true', 'True')
            return Token(TokenType.BOOLEAN, value, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负绌哄€?        if segment == '绌?:
            return Token(TokenType.NULL, None, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负鏁板瓧
        if segment.isdigit() or (segment.replace('.', '', 1).isdigit() and segment.count('.') == 1):
            try:
                if '.' in segment:
                    value = float(segment)
                else:
                    value = int(segment)
                return Token(TokenType.NUMBER, value, line_num, column, segment)
            except ValueError:
                pass
        
        # 妫€鏌ユ槸鍚︿负涓枃鏁板瓧
        if all(c in self.chinese_numbers for c in segment):
            value = self._chinese_to_arabic(segment)
            return Token(TokenType.CHINESE_NUMBER, value, line_num, column, segment)
        
        # 鏅€氭爣璇嗙
        return Token(TokenType.IDENTIFIER, segment, line_num, column, segment)
    
    def _parse_string_literal(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽瀛楃涓插瓧闈㈤噺"""
        quote_char = line[start]
        position = start + 1
        value = ''
        
        while position < len(line):
            char = line[position]
            
            if char == quote_char:
                # 缁撴潫寮曞彿
                position += 1
                break
            elif char == '\\' and position + 1 < len(line):
                # 杞箟瀛楃
                next_char = line[position + 1]
                if next_char in ('n', 't', '\\', '"', "'"):
                    value += self._escape_char(next_char)
                    position += 2
                else:
                    value += char
                    position += 1
            else:
                value += char
                position += 1
        
        lexeme = line[start:position]
        return Token(TokenType.STRING, value, line_num, column, lexeme)
    
    def _escape_char(self, char: str) -> str:
        """杞箟瀛楃"""
        escape_map = {
            'n': '\n',
            't': '\t',
            '\\': '\\',
            '"': '"',
            "'": "'",
        }
        return escape_map.get(char, char)
    
    def _parse_number(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽鏁板瓧瀛楅潰閲?""
        position = start
        
        # 瑙ｆ瀽鏁存暟閮ㄥ垎
        while position < len(line) and line[position].isdigit():
            position += 1
        
        # 瑙ｆ瀽灏忔暟閮ㄥ垎
        if position < len(line) and line[position] == '.':
            position += 1
            while position < len(line) and line[position].isdigit():
                position += 1
        
        # 瑙ｆ瀽绉戝璁℃暟娉?        if position < len(line) and line[position].lower() == 'e':
            position += 1
            if position < len(line) and line[position] in ('+', '-'):
                position += 1
            while position < len(line) and line[position].isdigit():
                position += 1
        
        lexeme = line[start:position]
        
        # 灏濊瘯杞崲涓烘暟瀛?        try:
            if '.' in lexeme or 'e' in lexeme.lower():
                value = float(lexeme)
            else:
                value = int(lexeme)
        except ValueError:
            value = lexeme  # 淇濇寔鍘熸牱
        
        return Token(TokenType.NUMBER, value, line_num, column, lexeme)
    
    def _parse_chinese_number(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽涓枃鏁板瓧"""
        position = start
        lexeme = ''
        
        while position < len(line) and line[position] in self.chinese_numbers:
            lexeme += line[position]
            position += 1
        
        # 杞崲涓洪樋鎷変集鏁板瓧
        value = self._chinese_to_arabic(lexeme)
        
        return Token(TokenType.CHINESE_NUMBER, value, line_num, column, lexeme)
    
    def _chinese_to_arabic(self, chinese_num: str) -> int:
        """灏嗕腑鏂囨暟瀛楄浆鎹负闃挎媺浼暟瀛?""
        if not chinese_num:
            return 0
        
        # 绠€鍗曞疄鐜帮紝鍙鐞嗗熀鏈暟瀛?        total = 0
        current = 0
        
        for char in chinese_num:
            num = self.chinese_numbers.get(char, 0)
            
            if num < 10:
                current = num
            elif num >= 10:
                if current == 0:
                    current = 1
                total += current * num
                current = 0
        
        total += current
        return total
    
    def _parse_identifier(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽鏍囪瘑绗?""
        position = start
        
        # 鏀堕泦鏍囪瘑绗﹀瓧绗?        while position < len(line) and self._is_identifier_char(line[position]):
            position += 1
        
        lexeme = line[start:position]
        
        # 妫€鏌ユ槸鍚︿负鍏抽敭璇?        token_type = self._get_keyword_type(lexeme)
        if token_type:
            return Token(token_type, lexeme, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负鐧惧濮撳彉閲?        if self._is_bai_jia_xing(lexeme):
            return Token(TokenType.BAIJIAXING, lexeme, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负鍔ㄨ瘝
        arity = get_verb_arity(lexeme)
        if arity != 0:
            # 鏍规嵁鍏冩暟纭畾鍔ㄨ瘝绫诲瀷
            if arity == -1:
                token_type = TokenType.VERB_VAR
            elif arity == 0:
                token_type = TokenType.VERB_0
            elif arity == 1:
                token_type = TokenType.VERB_1
            elif arity == 2:
                token_type = TokenType.VERB_2
            elif arity == 3:
                token_type = TokenType.VERB_3
            else:
                token_type = TokenType.VERB_VAR
            
            return Token(token_type, lexeme, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负甯冨皵瀛楅潰閲?        if lexeme in ('鐪?, '鍋?, 'true', 'false', 'True', 'False'):
            value = lexeme in ('鐪?, 'true', 'True')
            return Token(TokenType.BOOLEAN, value, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负绌哄€?        if lexeme == '绌?:
            return Token(TokenType.NULL, None, line_num, column, lexeme)
        
        # 灏濊瘯涓枃鍒嗚瘝
        if len(lexeme) > 1 and any('\u4e00' <= c <= '\u9fff' for c in lexeme):
            # 浣跨敤jieba杩涜涓枃鍒嗚瘝
            segments = self._segment(lexeme)
            if len(segments) > 1:
                # 濡傛灉鏄涓瘝锛岃繑鍥炵涓€涓瘝浣滀负鏍囪瘑绗?                first_segment = segments[0]
                # 閫掑綊澶勭悊绗竴涓瘝
                return self._parse_identifier(first_segment, 0, line_num, column)
        
        # 鏅€氭爣璇嗙
        return Token(TokenType.IDENTIFIER, lexeme, line_num, column, lexeme)
    
    def _is_identifier_char(self, char: str) -> bool:
        """妫€鏌ュ瓧绗︽槸鍚︿负鏍囪瘑绗﹀瓧绗?""
        # 涓枃瀛楃銆佽嫳鏂囧瓧姣嶃€佹暟瀛椼€佷笅鍒掔嚎
        return ('\u4e00' <= char <= '\u9fff' or
                'a' <= char <= 'z' or
                'A' <= char <= 'Z' or
                char.isdigit() or
                char == '_')
    
    def _get_keyword_type(self, lexeme: str) -> Optional[TokenType]:
        """鑾峰彇鍏抽敭璇嶇被鍨?""
        # 妫€鏌ョ姸鎬佸叧閿瘝锛堝瀛楋級
        for keyword, token_type in self.state_keywords.items():
            if lexeme.startswith(keyword):
                return token_type
        
        # 妫€鏌ユ劅鐭ュ叧閿瘝锛堝瀛楋級
        for keyword, token_type in self.perception_keywords.items():
            if lexeme.startswith(keyword):
                return token_type
        
        # 妫€鏌ユ椂闂村叧閿瘝锛堝瀛楋級
        for keyword, token_type in self.time_keywords.items():
            if lexeme.startswith(keyword):
                return token_type
        
        # 妫€鏌ユ櫘閫氬叧閿瘝
        return self.keywords.get(lexeme)
    
    def _is_bai_jia_xing(self, lexeme: str) -> bool:
        """妫€鏌ユ槸鍚︿负鐧惧濮撳彉閲?""
        if not lexeme:
            return False
        
        # 鑾峰彇濮撴皬锛堢涓€涓瓧绗︼級
        surname = lexeme[0]
        
        # 妫€鏌ユ槸鍚︿负鍐茬獊濮撴皬
        if surname in self.conflict_surnames:
            return False
        
        # 妫€鏌ユ槸鍚︿负鐧惧濮?        return surname in self.bai_jia_xing
    
    def print_tokens(self, tokens: List[Token]) -> None:
        """鎵撳嵃璇嶆硶鍗曞厓鍒楄〃"""
        print("璇嶆硶鍒嗘瀽缁撴灉:")
        print("=" * 80)
        print(f"{'琛?:<4} {'鍒?:<4} {'绫诲瀷':<20} {'鍊?:<20} {'璇嶇礌':<20}")
        print("-" * 80)
        
        for token in tokens:
            value_str = str(token.value)
            if len(value_str) > 18:
                value_str = value_str[:15] + "..."
            
            lexeme_str = token.lexeme
            if len(lexeme_str) > 18:
                lexeme_str = lexeme_str[:15] + "..."
            
            print(f"{token.line:<4} {token.column:<4} {token.type.value:<20} {value_str:<20} {lexeme_str:<20}")
        
        print("=" * 80)


# 娴嬭瘯鍑芥暟
def test_lexer():
    """娴嬭瘯璇嶆硶鍒嗘瀽鍣?""
    print("璇嶆硶鍒嗘瀽鍣ㄦ祴璇?)
    print("=" * 50)
    
    lexer = YanLuLexer()
    
    # 娴嬭瘯鐢ㄤ緥
    test_cases = [
        (
            "瀹氭俯搴︽槸25銆?,
            "鍙橀噺瀹氫箟"
        ),
        (
            "濡傛灉娓╁害澶?0灏卞紑鍚鎵囥€?,
            "鏉′欢璇彞"
        ),
        (
            "瀵逛簬i鍦?鍒?0锛氬嵃i銆?,
            "寰幆璇彞"
        ),
        (
            "娓╁害鍙樹负30搴︺€?,
            "鐘舵€佽浆鎹?
        ),
        (
            "寮犱笁銆佹潕鍥涳紝璁＄畻鎶樻墸銆?,
            "鎰忓悎寮忓嚱鏁拌皟鐢?
        ),
        (
            "'浣犲ソ锛屼笘鐣?",
            "瀛楃涓插瓧闈㈤噺"
        ),
        (
            "鐪熶笖鍋?,
            "甯冨皵杩愮畻"
        ),
        (
            "瀹歺绛変簬鍗佸姞浜斻€?,
            "涓枃鏁板瓧"
        ),
    ]
    
    for source_code, description in test_cases:
        print(f"\n娴嬭瘯: {description}")
        print(f"婧愪唬鐮? {source_code}")
        
        try:
            tokens = lexer.tokenize(source_code)
            lexer.print_tokens(tokens)
        except Exception as e:
            print(f"閿欒: {e}")
    
    print("=" * 50)
    print("娴嬭瘯瀹屾垚")


if __name__ == "__main__":
    test_lexer())
        self.identifier_pattern = re.compile(r'^[\u4e00-\u9fffA-Za-z_][\u4e00-\u9fffA-Za-z0-9_]*
        灏嗘簮浠ｇ爜杞崲涓鸿瘝娉曞崟鍏冨垪琛?        
        Args:
            source_code: 婧愪唬鐮佸瓧绗︿覆
            
        Returns:
            璇嶆硶鍗曞厓鍒楄〃
        """
        tokens = []
        lines = source_code.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            line_tokens = self._tokenize_line(line, line_num)
            tokens.extend(line_tokens)
            
            # 娣诲姞鎹㈣绗︼紙闄ら潪鏄渶鍚庝竴琛岋級
            if line_num < len(lines):
                tokens.append(Token(TokenType.NEWLINE, '\n', line_num, len(line) + 1, '\n'))
        
        # 娣诲姞鏂囦欢缁撴潫鏍囪
        tokens.append(Token(TokenType.EOF, '', len(lines) + 1, 1, ''))
        
        return tokens
    
    def _tokenize_line(self, line: str, line_num: int) -> List[Token]:
        """灏嗕竴琛屼唬鐮佽浆鎹负璇嶆硶鍗曞厓鍒楄〃"""
        tokens = []
        position = 0
        column = 1
        
        # 浣跨敤鍒嗚瘝鍣ㄨ繘琛屼腑鏂囧垎璇?        segments = self._segment(line)
        segment_index = 0
        
        while position < len(line):
            # 璺宠繃绌虹櫧瀛楃
            if line[position].isspace():
                if line[position] == '\n':
                    tokens.append(Token(TokenType.NEWLINE, '\n', line_num, column, '\n'))
                position += 1
                column += 1
                continue
            
            # 澶勭悊娉ㄩ噴
            if line[position] == '#':
                # 鍗曡娉ㄩ噴锛岃烦杩囨暣琛?                comment = line[position:]
                tokens.append(Token(TokenType.COMMENT, comment, line_num, column, comment))
                break
            
            # 澶勭悊澶氳瑷€浠ｇ爜鍧?            if line[position:position+2] == '{{':
                tokens.append(Token(TokenType.CODE_BLOCK_START, '{{', line_num, column, '{{'))
                position += 2
                column += 2
                continue
            
            if line[position:position+2] == '}}':
                tokens.append(Token(TokenType.CODE_BLOCK_END, '}}', line_num, column, '}}'))
                position += 2
                column += 2
                continue
            
            # 澶勭悊涓枃鏍囩偣绗﹀彿
            if line[position] in self.chinese_punctuation:
                char = line[position]
                token_type = self.chinese_punctuation[char]
                
                # 澶勭悊鎴愬鏍囩偣绗﹀彿
                if char in ('銆?, '銆?):
                    # 鏌ユ壘鍖归厤鐨勭粨鏉熺鍙?                    end_pos = line.find('銆? if char == '銆? else '銆?, position + 1)
                    if end_pos != -1:
                        value = line[position:end_pos + 1]
                        tokens.append(Token(token_type, value, line_num, column, value))
                        position = end_pos + 1
                        column += len(value)
                        continue
                
                tokens.append(Token(token_type, char, line_num, column, char))
                position += 1
                column += 1
                continue
            
            # 澶勭悊鐪佺暐鍙?            if line[position:position+2] == '鈥︹€?:
                tokens.append(Token(TokenType.ELLIPSIS, '鈥︹€?, line_num, column, '鈥︹€?))
                position += 2
                column += 2
                continue
            
            # 澶勭悊鐮存姌鍙?            if line[position:position+2] == '鈥斺€?:
                tokens.append(Token(TokenType.DASH, '鈥斺€?, line_num, column, '鈥斺€?))
                position += 2
                column += 2
                continue
            
            # 澶勭悊鍦嗗湀鍙?            if line[position] in '鈶犫憽鈶⑩懀鈶も懃鈶︹懅鈶ㄢ懇':
                tokens.append(Token(TokenType.CIRCLED_NUMBERS, line[position], line_num, column, line[position]))
                position += 1
                column += 1
                continue
            
            # 澶勭悊杩愮畻绗?            if line[position] in self.operators:
                # 妫€鏌ュ弻瀛楃杩愮畻绗?                if position + 1 < len(line):
                    two_char = line[position:position+2]
                    if two_char in ('鈮?, '鈮?, '鈮?):
                        tokens.append(Token(self.operators[two_char], two_char, line_num, column, two_char))
                        position += 2
                        column += 2
                        continue
                
                tokens.append(Token(self.operators[line[position]], line[position], line_num, column, line[position]))
                position += 1
                column += 1
                continue
            
            # 澶勭悊鍒嗙粍绗﹀彿
            if line[position] in self.grouping_symbols:
                tokens.append(Token(self.grouping_symbols[line[position]], line[position], line_num, column, line[position]))
                position += 1
                column += 1
                continue
            
            # 澶勭悊瀛楃涓插瓧闈㈤噺
            if line[position] in ('"', "'"):
                string_token = self._parse_string_literal(line, position, line_num, column)
                tokens.append(string_token)
                position += len(string_token.lexeme)
                column += len(string_token.lexeme)
                continue
            
            # 澶勭悊鏁板瓧瀛楅潰閲?            if line[position].isdigit() or (line[position] == '.' and position + 1 < len(line) and line[position + 1].isdigit()):
                number_token = self._parse_number(line, position, line_num, column)
                tokens.append(number_token)
                position += len(number_token.lexeme)
                column += len(number_token.lexeme)
                continue
            
            # 澶勭悊涓枃鏁板瓧
            if line[position] in self.chinese_numbers:
                chinese_number_token = self._parse_chinese_number(line, position, line_num, column)
                tokens.append(chinese_number_token)
                position += len(chinese_number_token.lexeme)
                column += len(chinese_number_token.lexeme)
                continue
            
            # 澶勭悊褰撳墠鍒嗚瘝娈?            if segment_index < len(segments):
                segment = segments[segment_index].strip()
                if segment:  # 璺宠繃绌哄垎璇?                    # 澶勭悊鍒嗚瘝娈?                    token = self._process_segment(segment, line_num, column)
                    tokens.append(token)
                    position += len(segment)
                    column += len(segment)
                segment_index += 1
            else:
                # 濡傛灉娌℃湁鏇村鍒嗚瘝锛屽鐞嗗墿浣欏瓧绗?                identifier_token = self._parse_identifier(line, position, line_num, column)
                tokens.append(identifier_token)
                position += len(identifier_token.lexeme)
                column += len(identifier_token.lexeme)
        
        return tokens
    
    def _process_segment(self, segment: str, line_num: int, column: int) -> Token:
        """澶勭悊鍒嗚瘝娈?""
        # 妫€鏌ユ槸鍚︿负鍏抽敭璇?        token_type = self._get_keyword_type(segment)
        if token_type:
            return Token(token_type, segment, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负鐧惧濮撳彉閲?        if self._is_bai_jia_xing(segment):
            return Token(TokenType.BAIJIAXING, segment, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负鍔ㄨ瘝
        arity = get_verb_arity(segment)
        if arity != 0:
            # 鏍规嵁鍏冩暟纭畾鍔ㄨ瘝绫诲瀷
            if arity == -1:
                token_type = TokenType.VERB_VAR
            elif arity == 0:
                token_type = TokenType.VERB_0
            elif arity == 1:
                token_type = TokenType.VERB_1
            elif arity == 2:
                token_type = TokenType.VERB_2
            elif arity == 3:
                token_type = TokenType.VERB_3
            else:
                token_type = TokenType.VERB_VAR
            
            return Token(token_type, segment, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负甯冨皵瀛楅潰閲?        if segment in ('鐪?, '鍋?, 'true', 'false', 'True', 'False'):
            value = segment in ('鐪?, 'true', 'True')
            return Token(TokenType.BOOLEAN, value, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负绌哄€?        if segment == '绌?:
            return Token(TokenType.NULL, None, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负鏁板瓧
        if segment.isdigit() or (segment.replace('.', '', 1).isdigit() and segment.count('.') == 1):
            try:
                if '.' in segment:
                    value = float(segment)
                else:
                    value = int(segment)
                return Token(TokenType.NUMBER, value, line_num, column, segment)
            except ValueError:
                pass
        
        # 妫€鏌ユ槸鍚︿负涓枃鏁板瓧
        if all(c in self.chinese_numbers for c in segment):
            value = self._chinese_to_arabic(segment)
            return Token(TokenType.CHINESE_NUMBER, value, line_num, column, segment)
        
        # 鏅€氭爣璇嗙
        return Token(TokenType.IDENTIFIER, segment, line_num, column, segment)
    
    def _parse_string_literal(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽瀛楃涓插瓧闈㈤噺"""
        quote_char = line[start]
        position = start + 1
        value = ''
        
        while position < len(line):
            char = line[position]
            
            if char == quote_char:
                # 缁撴潫寮曞彿
                position += 1
                break
            elif char == '\\' and position + 1 < len(line):
                # 杞箟瀛楃
                next_char = line[position + 1]
                if next_char in ('n', 't', '\\', '"', "'"):
                    value += self._escape_char(next_char)
                    position += 2
                else:
                    value += char
                    position += 1
            else:
                value += char
                position += 1
        
        lexeme = line[start:position]
        return Token(TokenType.STRING, value, line_num, column, lexeme)
    
    def _escape_char(self, char: str) -> str:
        """杞箟瀛楃"""
        escape_map = {
            'n': '\n',
            't': '\t',
            '\\': '\\',
            '"': '"',
            "'": "'",
        }
        return escape_map.get(char, char)
    
    def _parse_number(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽鏁板瓧瀛楅潰閲?""
        position = start
        
        # 瑙ｆ瀽鏁存暟閮ㄥ垎
        while position < len(line) and line[position].isdigit():
            position += 1
        
        # 瑙ｆ瀽灏忔暟閮ㄥ垎
        if position < len(line) and line[position] == '.':
            position += 1
            while position < len(line) and line[position].isdigit():
                position += 1
        
        # 瑙ｆ瀽绉戝璁℃暟娉?        if position < len(line) and line[position].lower() == 'e':
            position += 1
            if position < len(line) and line[position] in ('+', '-'):
                position += 1
            while position < len(line) and line[position].isdigit():
                position += 1
        
        lexeme = line[start:position]
        
        # 灏濊瘯杞崲涓烘暟瀛?        try:
            if '.' in lexeme or 'e' in lexeme.lower():
                value = float(lexeme)
            else:
                value = int(lexeme)
        except ValueError:
            value = lexeme  # 淇濇寔鍘熸牱
        
        return Token(TokenType.NUMBER, value, line_num, column, lexeme)
    
    def _parse_chinese_number(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽涓枃鏁板瓧"""
        position = start
        lexeme = ''
        
        while position < len(line) and line[position] in self.chinese_numbers:
            lexeme += line[position]
            position += 1
        
        # 杞崲涓洪樋鎷変集鏁板瓧
        value = self._chinese_to_arabic(lexeme)
        
        return Token(TokenType.CHINESE_NUMBER, value, line_num, column, lexeme)
    
    def _chinese_to_arabic(self, chinese_num: str) -> int:
        """灏嗕腑鏂囨暟瀛楄浆鎹负闃挎媺浼暟瀛?""
        if not chinese_num:
            return 0
        
        # 绠€鍗曞疄鐜帮紝鍙鐞嗗熀鏈暟瀛?        total = 0
        current = 0
        
        for char in chinese_num:
            num = self.chinese_numbers.get(char, 0)
            
            if num < 10:
                current = num
            elif num >= 10:
                if current == 0:
                    current = 1
                total += current * num
                current = 0
        
        total += current
        return total
    
    def _parse_identifier(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽鏍囪瘑绗?""
        position = start
        
        # 鏀堕泦鏍囪瘑绗﹀瓧绗?        while position < len(line) and self._is_identifier_char(line[position]):
            position += 1
        
        lexeme = line[start:position]
        
        # 妫€鏌ユ槸鍚︿负鍏抽敭璇?        token_type = self._get_keyword_type(lexeme)
        if token_type:
            return Token(token_type, lexeme, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负鐧惧濮撳彉閲?        if self._is_bai_jia_xing(lexeme):
            return Token(TokenType.BAIJIAXING, lexeme, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负鍔ㄨ瘝
        arity = get_verb_arity(lexeme)
        if arity != 0:
            # 鏍规嵁鍏冩暟纭畾鍔ㄨ瘝绫诲瀷
            if arity == -1:
                token_type = TokenType.VERB_VAR
            elif arity == 0:
                token_type = TokenType.VERB_0
            elif arity == 1:
                token_type = TokenType.VERB_1
            elif arity == 2:
                token_type = TokenType.VERB_2
            elif arity == 3:
                token_type = TokenType.VERB_3
            else:
                token_type = TokenType.VERB_VAR
            
            return Token(token_type, lexeme, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负甯冨皵瀛楅潰閲?        if lexeme in ('鐪?, '鍋?, 'true', 'false', 'True', 'False'):
            value = lexeme in ('鐪?, 'true', 'True')
            return Token(TokenType.BOOLEAN, value, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负绌哄€?        if lexeme == '绌?:
            return Token(TokenType.NULL, None, line_num, column, lexeme)
        
        # 灏濊瘯涓枃鍒嗚瘝
        if len(lexeme) > 1 and any('\u4e00' <= c <= '\u9fff' for c in lexeme):
            # 浣跨敤jieba杩涜涓枃鍒嗚瘝
            segments = self._segment(lexeme)
            if len(segments) > 1:
                # 濡傛灉鏄涓瘝锛岃繑鍥炵涓€涓瘝浣滀负鏍囪瘑绗?                first_segment = segments[0]
                # 閫掑綊澶勭悊绗竴涓瘝
                return self._parse_identifier(first_segment, 0, line_num, column)
        
        # 鏅€氭爣璇嗙
        return Token(TokenType.IDENTIFIER, lexeme, line_num, column, lexeme)
    
    def _is_identifier_char(self, char: str) -> bool:
        """妫€鏌ュ瓧绗︽槸鍚︿负鏍囪瘑绗﹀瓧绗?""
        # 涓枃瀛楃銆佽嫳鏂囧瓧姣嶃€佹暟瀛椼€佷笅鍒掔嚎
        return ('\u4e00' <= char <= '\u9fff' or
                'a' <= char <= 'z' or
                'A' <= char <= 'Z' or
                char.isdigit() or
                char == '_')
    
    def _get_keyword_type(self, lexeme: str) -> Optional[TokenType]:
        """鑾峰彇鍏抽敭璇嶇被鍨?""
        # 妫€鏌ョ姸鎬佸叧閿瘝锛堝瀛楋級
        for keyword, token_type in self.state_keywords.items():
            if lexeme.startswith(keyword):
                return token_type
        
        # 妫€鏌ユ劅鐭ュ叧閿瘝锛堝瀛楋級
        for keyword, token_type in self.perception_keywords.items():
            if lexeme.startswith(keyword):
                return token_type
        
        # 妫€鏌ユ椂闂村叧閿瘝锛堝瀛楋級
        for keyword, token_type in self.time_keywords.items():
            if lexeme.startswith(keyword):
                return token_type
        
        # 妫€鏌ユ櫘閫氬叧閿瘝
        return self.keywords.get(lexeme)
    
    def _is_bai_jia_xing(self, lexeme: str) -> bool:
        """妫€鏌ユ槸鍚︿负鐧惧濮撳彉閲?""
        if not lexeme:
            return False
        
        # 鑾峰彇濮撴皬锛堢涓€涓瓧绗︼級
        surname = lexeme[0]
        
        # 妫€鏌ユ槸鍚︿负鍐茬獊濮撴皬
        if surname in self.conflict_surnames:
            return False
        
        # 妫€鏌ユ槸鍚︿负鐧惧濮?        return surname in self.bai_jia_xing
    
    def print_tokens(self, tokens: List[Token]) -> None:
        """鎵撳嵃璇嶆硶鍗曞厓鍒楄〃"""
        print("璇嶆硶鍒嗘瀽缁撴灉:")
        print("=" * 80)
        print(f"{'琛?:<4} {'鍒?:<4} {'绫诲瀷':<20} {'鍊?:<20} {'璇嶇礌':<20}")
        print("-" * 80)
        
        for token in tokens:
            value_str = str(token.value)
            if len(value_str) > 18:
                value_str = value_str[:15] + "..."
            
            lexeme_str = token.lexeme
            if len(lexeme_str) > 18:
                lexeme_str = lexeme_str[:15] + "..."
            
            print(f"{token.line:<4} {token.column:<4} {token.type.value:<20} {value_str:<20} {lexeme_str:<20}")
        
        print("=" * 80)


# 娴嬭瘯鍑芥暟
def test_lexer():
    """娴嬭瘯璇嶆硶鍒嗘瀽鍣?""
    print("璇嶆硶鍒嗘瀽鍣ㄦ祴璇?)
    print("=" * 50)
    
    lexer = YanLuLexer()
    
    # 娴嬭瘯鐢ㄤ緥
    test_cases = [
        (
            "瀹氭俯搴︽槸25銆?,
            "鍙橀噺瀹氫箟"
        ),
        (
            "濡傛灉娓╁害澶?0灏卞紑鍚鎵囥€?,
            "鏉′欢璇彞"
        ),
        (
            "瀵逛簬i鍦?鍒?0锛氬嵃i銆?,
            "寰幆璇彞"
        ),
        (
            "娓╁害鍙樹负30搴︺€?,
            "鐘舵€佽浆鎹?
        ),
        (
            "寮犱笁銆佹潕鍥涳紝璁＄畻鎶樻墸銆?,
            "鎰忓悎寮忓嚱鏁拌皟鐢?
        ),
        (
            "'浣犲ソ锛屼笘鐣?",
            "瀛楃涓插瓧闈㈤噺"
        ),
        (
            "鐪熶笖鍋?,
            "甯冨皵杩愮畻"
        ),
        (
            "瀹歺绛変簬鍗佸姞浜斻€?,
            "涓枃鏁板瓧"
        ),
    ]
    
    for source_code, description in test_cases:
        print(f"\n娴嬭瘯: {description}")
        print(f"婧愪唬鐮? {source_code}")
        
        try:
            tokens = lexer.tokenize(source_code)
            lexer.print_tokens(tokens)
        except Exception as e:
            print(f"閿欒: {e}")
    
    print("=" * 50)
    print("娴嬭瘯瀹屾垚")


if __name__ == "__main__":
    test_lexer())
        self.identifier_pattern = re.compile(r'^[\u4e00-\u9fffA-Za-z_][\u4e00-\u9fffA-Za-z0-9_]*
        """
        灏嗘簮浠ｇ爜杞崲涓鸿瘝娉曞崟鍏冨垪琛?        
        Args:
            source_code: 婧愪唬鐮佸瓧绗︿覆
            
        Returns:
            璇嶆硶鍗曞厓鍒楄〃
        """
        tokens = []
        lines = source_code.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            line_tokens = self._tokenize_line(line, line_num)
            tokens.extend(line_tokens)
            
            # 娣诲姞鎹㈣绗︼紙闄ら潪鏄渶鍚庝竴琛岋級
            if line_num < len(lines):
                tokens.append(Token(TokenType.NEWLINE, '\n', line_num, len(line) + 1, '\n'))
        
        # 娣诲姞鏂囦欢缁撴潫鏍囪
        tokens.append(Token(TokenType.EOF, '', len(lines) + 1, 1, ''))
        
        return tokens
    
    def _tokenize_line(self, line: str, line_num: int) -> List[Token]:
        """灏嗕竴琛屼唬鐮佽浆鎹负璇嶆硶鍗曞厓鍒楄〃"""
        tokens = []
        position = 0
        column = 1
        
        # 浣跨敤鍒嗚瘝鍣ㄨ繘琛屼腑鏂囧垎璇?        segments = self._segment(line)
        segment_index = 0
        
        while position < len(line):
            # 璺宠繃绌虹櫧瀛楃
            if line[position].isspace():
                if line[position] == '\n':
                    tokens.append(Token(TokenType.NEWLINE, '\n', line_num, column, '\n'))
                position += 1
                column += 1
                continue
            
            # 澶勭悊娉ㄩ噴
            if line[position] == '#':
                # 鍗曡娉ㄩ噴锛岃烦杩囨暣琛?                comment = line[position:]
                tokens.append(Token(TokenType.COMMENT, comment, line_num, column, comment))
                break
            
            # 澶勭悊澶氳瑷€浠ｇ爜鍧?            if line[position:position+2] == '{{':
                tokens.append(Token(TokenType.CODE_BLOCK_START, '{{', line_num, column, '{{'))
                position += 2
                column += 2
                continue
            
            if line[position:position+2] == '}}':
                tokens.append(Token(TokenType.CODE_BLOCK_END, '}}', line_num, column, '}}'))
                position += 2
                column += 2
                continue
            
            # 澶勭悊涓枃鏍囩偣绗﹀彿
            if line[position] in self.chinese_punctuation:
                char = line[position]
                token_type = self.chinese_punctuation[char]
                
                # 澶勭悊鎴愬鏍囩偣绗﹀彿
                if char in ('銆?, '銆?):
                    # 鏌ユ壘鍖归厤鐨勭粨鏉熺鍙?                    end_pos = line.find('銆? if char == '銆? else '銆?, position + 1)
                    if end_pos != -1:
                        value = line[position:end_pos + 1]
                        tokens.append(Token(token_type, value, line_num, column, value))
                        position = end_pos + 1
                        column += len(value)
                        continue
                
                tokens.append(Token(token_type, char, line_num, column, char))
                position += 1
                column += 1
                continue
            
            # 澶勭悊鐪佺暐鍙?            if line[position:position+2] == '鈥︹€?:
                tokens.append(Token(TokenType.ELLIPSIS, '鈥︹€?, line_num, column, '鈥︹€?))
                position += 2
                column += 2
                continue
            
            # 澶勭悊鐮存姌鍙?            if line[position:position+2] == '鈥斺€?:
                tokens.append(Token(TokenType.DASH, '鈥斺€?, line_num, column, '鈥斺€?))
                position += 2
                column += 2
                continue
            
            # 澶勭悊鍦嗗湀鍙?            if line[position] in '鈶犫憽鈶⑩懀鈶も懃鈶︹懅鈶ㄢ懇':
                tokens.append(Token(TokenType.CIRCLED_NUMBERS, line[position], line_num, column, line[position]))
                position += 1
                column += 1
                continue
            
            # 澶勭悊杩愮畻绗?            if line[position] in self.operators:
                # 妫€鏌ュ弻瀛楃杩愮畻绗?                if position + 1 < len(line):
                    two_char = line[position:position+2]
                    if two_char in ('鈮?, '鈮?, '鈮?):
                        tokens.append(Token(self.operators[two_char], two_char, line_num, column, two_char))
                        position += 2
                        column += 2
                        continue
                
                tokens.append(Token(self.operators[line[position]], line[position], line_num, column, line[position]))
                position += 1
                column += 1
                continue
            
            # 澶勭悊鍒嗙粍绗﹀彿
            if line[position] in self.grouping_symbols:
                tokens.append(Token(self.grouping_symbols[line[position]], line[position], line_num, column, line[position]))
                position += 1
                column += 1
                continue
            
            # 澶勭悊瀛楃涓插瓧闈㈤噺
            if line[position] in ('"', "'"):
                string_token = self._parse_string_literal(line, position, line_num, column)
                tokens.append(string_token)
                position += len(string_token.lexeme)
                column += len(string_token.lexeme)
                continue
            
            # 澶勭悊鏁板瓧瀛楅潰閲?            if line[position].isdigit() or (line[position] == '.' and position + 1 < len(line) and line[position + 1].isdigit()):
                number_token = self._parse_number(line, position, line_num, column)
                tokens.append(number_token)
                position += len(number_token.lexeme)
                column += len(number_token.lexeme)
                continue
            
            # 澶勭悊涓枃鏁板瓧
            if line[position] in self.chinese_numbers:
                chinese_number_token = self._parse_chinese_number(line, position, line_num, column)
                tokens.append(chinese_number_token)
                position += len(chinese_number_token.lexeme)
                column += len(chinese_number_token.lexeme)
                continue
            
            # 澶勭悊褰撳墠鍒嗚瘝娈?            if segment_index < len(segments):
                segment = segments[segment_index].strip()
                if segment:  # 璺宠繃绌哄垎璇?                    # 澶勭悊鍒嗚瘝娈?                    token = self._process_segment(segment, line_num, column)
                    tokens.append(token)
                    position += len(segment)
                    column += len(segment)
                segment_index += 1
            else:
                # 濡傛灉娌℃湁鏇村鍒嗚瘝锛屽鐞嗗墿浣欏瓧绗?                identifier_token = self._parse_identifier(line, position, line_num, column)
                tokens.append(identifier_token)
                position += len(identifier_token.lexeme)
                column += len(identifier_token.lexeme)
        
        return tokens
    
    def _process_segment(self, segment: str, line_num: int, column: int) -> Token:
        """澶勭悊鍒嗚瘝娈?""
        # 妫€鏌ユ槸鍚︿负鍏抽敭璇?        token_type = self._get_keyword_type(segment)
        if token_type:
            return Token(token_type, segment, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负鐧惧濮撳彉閲?        if self._is_bai_jia_xing(segment):
            return Token(TokenType.BAIJIAXING, segment, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负鍔ㄨ瘝
        arity = get_verb_arity(segment)
        if arity != 0:
            # 鏍规嵁鍏冩暟纭畾鍔ㄨ瘝绫诲瀷
            if arity == -1:
                token_type = TokenType.VERB_VAR
            elif arity == 0:
                token_type = TokenType.VERB_0
            elif arity == 1:
                token_type = TokenType.VERB_1
            elif arity == 2:
                token_type = TokenType.VERB_2
            elif arity == 3:
                token_type = TokenType.VERB_3
            else:
                token_type = TokenType.VERB_VAR
            
            return Token(token_type, segment, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负甯冨皵瀛楅潰閲?        if segment in ('鐪?, '鍋?, 'true', 'false', 'True', 'False'):
            value = segment in ('鐪?, 'true', 'True')
            return Token(TokenType.BOOLEAN, value, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负绌哄€?        if segment == '绌?:
            return Token(TokenType.NULL, None, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负鏁板瓧
        if segment.isdigit() or (segment.replace('.', '', 1).isdigit() and segment.count('.') == 1):
            try:
                if '.' in segment:
                    value = float(segment)
                else:
                    value = int(segment)
                return Token(TokenType.NUMBER, value, line_num, column, segment)
            except ValueError:
                pass
        
        # 妫€鏌ユ槸鍚︿负涓枃鏁板瓧
        if all(c in self.chinese_numbers for c in segment):
            value = self._chinese_to_arabic(segment)
            return Token(TokenType.CHINESE_NUMBER, value, line_num, column, segment)
        
        # 鏅€氭爣璇嗙
        return Token(TokenType.IDENTIFIER, segment, line_num, column, segment)
    
    def _parse_string_literal(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽瀛楃涓插瓧闈㈤噺"""
        quote_char = line[start]
        position = start + 1
        value = ''
        
        while position < len(line):
            char = line[position]
            
            if char == quote_char:
                # 缁撴潫寮曞彿
                position += 1
                break
            elif char == '\\' and position + 1 < len(line):
                # 杞箟瀛楃
                next_char = line[position + 1]
                if next_char in ('n', 't', '\\', '"', "'"):
                    value += self._escape_char(next_char)
                    position += 2
                else:
                    value += char
                    position += 1
            else:
                value += char
                position += 1
        
        lexeme = line[start:position]
        return Token(TokenType.STRING, value, line_num, column, lexeme)
    
    def _escape_char(self, char: str) -> str:
        """杞箟瀛楃"""
        escape_map = {
            'n': '\n',
            't': '\t',
            '\\': '\\',
            '"': '"',
            "'": "'",
        }
        return escape_map.get(char, char)
    
    def _parse_number(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽鏁板瓧瀛楅潰閲?""
        position = start
        
        # 瑙ｆ瀽鏁存暟閮ㄥ垎
        while position < len(line) and line[position].isdigit():
            position += 1
        
        # 瑙ｆ瀽灏忔暟閮ㄥ垎
        if position < len(line) and line[position] == '.':
            position += 1
            while position < len(line) and line[position].isdigit():
                position += 1
        
        # 瑙ｆ瀽绉戝璁℃暟娉?        if position < len(line) and line[position].lower() == 'e':
            position += 1
            if position < len(line) and line[position] in ('+', '-'):
                position += 1
            while position < len(line) and line[position].isdigit():
                position += 1
        
        lexeme = line[start:position]
        
        # 灏濊瘯杞崲涓烘暟瀛?        try:
            if '.' in lexeme or 'e' in lexeme.lower():
                value = float(lexeme)
            else:
                value = int(lexeme)
        except ValueError:
            value = lexeme  # 淇濇寔鍘熸牱
        
        return Token(TokenType.NUMBER, value, line_num, column, lexeme)
    
    def _parse_chinese_number(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽涓枃鏁板瓧"""
        position = start
        lexeme = ''
        
        while position < len(line) and line[position] in self.chinese_numbers:
            lexeme += line[position]
            position += 1
        
        # 杞崲涓洪樋鎷変集鏁板瓧
        value = self._chinese_to_arabic(lexeme)
        
        return Token(TokenType.CHINESE_NUMBER, value, line_num, column, lexeme)
    
    def _chinese_to_arabic(self, chinese_num: str) -> int:
        """灏嗕腑鏂囨暟瀛楄浆鎹负闃挎媺浼暟瀛?""
        if not chinese_num:
            return 0
        
        # 绠€鍗曞疄鐜帮紝鍙鐞嗗熀鏈暟瀛?        total = 0
        current = 0
        
        for char in chinese_num:
            num = self.chinese_numbers.get(char, 0)
            
            if num < 10:
                current = num
            elif num >= 10:
                if current == 0:
                    current = 1
                total += current * num
                current = 0
        
        total += current
        return total
    
    def _parse_identifier(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽鏍囪瘑绗?""
        position = start
        
        # 鏀堕泦鏍囪瘑绗﹀瓧绗?        while position < len(line) and self._is_identifier_char(line[position]):
            position += 1
        
        lexeme = line[start:position]
        
        # 妫€鏌ユ槸鍚︿负鍏抽敭璇?        token_type = self._get_keyword_type(lexeme)
        if token_type:
            return Token(token_type, lexeme, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负鐧惧濮撳彉閲?        if self._is_bai_jia_xing(lexeme):
            return Token(TokenType.BAIJIAXING, lexeme, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负鍔ㄨ瘝
        arity = get_verb_arity(lexeme)
        if arity != 0:
            # 鏍规嵁鍏冩暟纭畾鍔ㄨ瘝绫诲瀷
            if arity == -1:
                token_type = TokenType.VERB_VAR
            elif arity == 0:
                token_type = TokenType.VERB_0
            elif arity == 1:
                token_type = TokenType.VERB_1
            elif arity == 2:
                token_type = TokenType.VERB_2
            elif arity == 3:
                token_type = TokenType.VERB_3
            else:
                token_type = TokenType.VERB_VAR
            
            return Token(token_type, lexeme, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负甯冨皵瀛楅潰閲?        if lexeme in ('鐪?, '鍋?, 'true', 'false', 'True', 'False'):
            value = lexeme in ('鐪?, 'true', 'True')
            return Token(TokenType.BOOLEAN, value, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负绌哄€?        if lexeme == '绌?:
            return Token(TokenType.NULL, None, line_num, column, lexeme)
        
        # 灏濊瘯涓枃鍒嗚瘝
        if len(lexeme) > 1 and any('\u4e00' <= c <= '\u9fff' for c in lexeme):
            # 浣跨敤jieba杩涜涓枃鍒嗚瘝
            segments = self._segment(lexeme)
            if len(segments) > 1:
                # 濡傛灉鏄涓瘝锛岃繑鍥炵涓€涓瘝浣滀负鏍囪瘑绗?                first_segment = segments[0]
                # 閫掑綊澶勭悊绗竴涓瘝
                return self._parse_identifier(first_segment, 0, line_num, column)
        
        # 鏅€氭爣璇嗙
        return Token(TokenType.IDENTIFIER, lexeme, line_num, column, lexeme)
    
    def _is_identifier_char(self, char: str) -> bool:
        """妫€鏌ュ瓧绗︽槸鍚︿负鏍囪瘑绗﹀瓧绗?""
        # 涓枃瀛楃銆佽嫳鏂囧瓧姣嶃€佹暟瀛椼€佷笅鍒掔嚎
        return ('\u4e00' <= char <= '\u9fff' or
                'a' <= char <= 'z' or
                'A' <= char <= 'Z' or
                char.isdigit() or
                char == '_')
    
    def _get_keyword_type(self, lexeme: str) -> Optional[TokenType]:
        """鑾峰彇鍏抽敭璇嶇被鍨?""
        # 妫€鏌ョ姸鎬佸叧閿瘝锛堝瀛楋級
        for keyword, token_type in self.state_keywords.items():
            if lexeme.startswith(keyword):
                return token_type
        
        # 妫€鏌ユ劅鐭ュ叧閿瘝锛堝瀛楋級
        for keyword, token_type in self.perception_keywords.items():
            if lexeme.startswith(keyword):
                return token_type
        
        # 妫€鏌ユ椂闂村叧閿瘝锛堝瀛楋級
        for keyword, token_type in self.time_keywords.items():
            if lexeme.startswith(keyword):
                return token_type
        
        # 妫€鏌ユ櫘閫氬叧閿瘝
        return self.keywords.get(lexeme)
    
    def _is_bai_jia_xing(self, lexeme: str) -> bool:
        """妫€鏌ユ槸鍚︿负鐧惧濮撳彉閲?""
        if not lexeme:
            return False
        
        # 鑾峰彇濮撴皬锛堢涓€涓瓧绗︼級
        surname = lexeme[0]
        
        # 妫€鏌ユ槸鍚︿负鍐茬獊濮撴皬
        if surname in self.conflict_surnames:
            return False
        
        # 妫€鏌ユ槸鍚︿负鐧惧濮?        return surname in self.bai_jia_xing
    
    def print_tokens(self, tokens: List[Token]) -> None:
        """鎵撳嵃璇嶆硶鍗曞厓鍒楄〃"""
        print("璇嶆硶鍒嗘瀽缁撴灉:")
        print("=" * 80)
        print(f"{'琛?:<4} {'鍒?:<4} {'绫诲瀷':<20} {'鍊?:<20} {'璇嶇礌':<20}")
        print("-" * 80)
        
        for token in tokens:
            value_str = str(token.value)
            if len(value_str) > 18:
                value_str = value_str[:15] + "..."
            
            lexeme_str = token.lexeme
            if len(lexeme_str) > 18:
                lexeme_str = lexeme_str[:15] + "..."
            
            print(f"{token.line:<4} {token.column:<4} {token.type.value:<20} {value_str:<20} {lexeme_str:<20}")
        
        print("=" * 80)


# 娴嬭瘯鍑芥暟
def test_lexer():
    """娴嬭瘯璇嶆硶鍒嗘瀽鍣?""
    print("璇嶆硶鍒嗘瀽鍣ㄦ祴璇?)
    print("=" * 50)
    
    lexer = YanLuLexer()
    
    # 娴嬭瘯鐢ㄤ緥
    test_cases = [
        (
            "瀹氭俯搴︽槸25銆?,
            "鍙橀噺瀹氫箟"
        ),
        (
            "濡傛灉娓╁害澶?0灏卞紑鍚鎵囥€?,
            "鏉′欢璇彞"
        ),
        (
            "瀵逛簬i鍦?鍒?0锛氬嵃i銆?,
            "寰幆璇彞"
        ),
        (
            "娓╁害鍙樹负30搴︺€?,
            "鐘舵€佽浆鎹?
        ),
        (
            "寮犱笁銆佹潕鍥涳紝璁＄畻鎶樻墸銆?,
            "鎰忓悎寮忓嚱鏁拌皟鐢?
        ),
        (
            "'浣犲ソ锛屼笘鐣?",
            "瀛楃涓插瓧闈㈤噺"
        ),
        (
            "鐪熶笖鍋?,
            "甯冨皵杩愮畻"
        ),
        (
            "瀹歺绛変簬鍗佸姞浜斻€?,
            "涓枃鏁板瓧"
        ),
    ]
    
    for source_code, description in test_cases:
        print(f"\n娴嬭瘯: {description}")
        print(f"婧愪唬鐮? {source_code}")
        
        try:
            tokens = lexer.tokenize(source_code)
            lexer.print_tokens(tokens)
        except Exception as e:
            print(f"閿欒: {e}")
    
    print("=" * 50)
    print("娴嬭瘯瀹屾垚")


if __name__ == "__main__":
    test_lexer())
    
    def _init_segmenter(self):
        """鍒濆鍖栧垎璇嶅櫒"""
        if self.segmenter_type == "thulac":
            try:
                import thulac
                # 浣跨敤seg_only=True鍙繘琛屽垎璇嶏紝涓嶈繘琛岃瘝鎬ф爣娉?                self.segmenter = thulac.thulac(seg_only=True, model_path=None)
                print(f"浣跨敤THULAC鍒嗚瘝鍣?(seg_only妯″紡)")
            except ImportError:
                print("璀﹀憡: 鏈畨瑁匱HULAC锛屽洖閫€鍒癹ieba鍒嗚瘝鍣?)
                print("瀹夎鍛戒护: pip install thulac")
                self.segmenter_type = "jieba"
                self.segmenter = jieba
        else:
            # 榛樿浣跨敤jieba
            self.segmenter = jieba
            print(f"浣跨敤jieba鍒嗚瘝鍣?)
    
    def _segment(self, text: str) -> List[str]:
        """
        鍒嗚瘝鏂规硶
        
        Args:
            text: 寰呭垎璇嶇殑鏂囨湰
            
        Returns:
            鍒嗚瘝缁撴灉鍒楄〃
        """
        if self.segmenter_type == "thulac":
            # THULAC鍒嗚瘝
            result = self.segmenter.cut(text, text=True)
            return result.split()
        else:
            # jieba鍒嗚瘝
            return list(self.segmenter.lcut(text))
        
    def tokenize(self, source_code: str) -> List[Token]:
        """
        灏嗘簮浠ｇ爜杞崲涓鸿瘝娉曞崟鍏冨垪琛?        
        Args:
            source_code: 婧愪唬鐮佸瓧绗︿覆
            
        Returns:
            璇嶆硶鍗曞厓鍒楄〃
        """
        tokens = []
        lines = source_code.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            line_tokens = self._tokenize_line(line, line_num)
            tokens.extend(line_tokens)
            
            # 娣诲姞鎹㈣绗︼紙闄ら潪鏄渶鍚庝竴琛岋級
            if line_num < len(lines):
                tokens.append(Token(TokenType.NEWLINE, '\n', line_num, len(line) + 1, '\n'))
        
        # 娣诲姞鏂囦欢缁撴潫鏍囪
        tokens.append(Token(TokenType.EOF, '', len(lines) + 1, 1, ''))
        
        return tokens
    
    def _tokenize_line(self, line: str, line_num: int) -> List[Token]:
        """灏嗕竴琛屼唬鐮佽浆鎹负璇嶆硶鍗曞厓鍒楄〃"""
        tokens = []
        position = 0
        column = 1
        
        # 浣跨敤鍒嗚瘝鍣ㄨ繘琛屼腑鏂囧垎璇?        segments = self._segment(line)
        segment_index = 0
        
        while position < len(line):
            # 璺宠繃绌虹櫧瀛楃
            if line[position].isspace():
                if line[position] == '\n':
                    tokens.append(Token(TokenType.NEWLINE, '\n', line_num, column, '\n'))
                position += 1
                column += 1
                continue
            
            # 澶勭悊娉ㄩ噴
            if line[position] == '#':
                # 鍗曡娉ㄩ噴锛岃烦杩囨暣琛?                comment = line[position:]
                tokens.append(Token(TokenType.COMMENT, comment, line_num, column, comment))
                break
            
            # 澶勭悊澶氳瑷€浠ｇ爜鍧?            if line[position:position+2] == '{{':
                tokens.append(Token(TokenType.CODE_BLOCK_START, '{{', line_num, column, '{{'))
                position += 2
                column += 2
                continue
            
            if line[position:position+2] == '}}':
                tokens.append(Token(TokenType.CODE_BLOCK_END, '}}', line_num, column, '}}'))
                position += 2
                column += 2
                continue
            
            # 澶勭悊涓枃鏍囩偣绗﹀彿
            if line[position] in self.chinese_punctuation:
                char = line[position]
                token_type = self.chinese_punctuation[char]
                
                # 澶勭悊鎴愬鏍囩偣绗﹀彿
                if char in ('銆?, '銆?):
                    # 鏌ユ壘鍖归厤鐨勭粨鏉熺鍙?                    end_pos = line.find('銆? if char == '銆? else '銆?, position + 1)
                    if end_pos != -1:
                        value = line[position:end_pos + 1]
                        tokens.append(Token(token_type, value, line_num, column, value))
                        position = end_pos + 1
                        column += len(value)
                        continue
                
                tokens.append(Token(token_type, char, line_num, column, char))
                position += 1
                column += 1
                continue
            
            # 澶勭悊鐪佺暐鍙?            if line[position:position+2] == '鈥︹€?:
                tokens.append(Token(TokenType.ELLIPSIS, '鈥︹€?, line_num, column, '鈥︹€?))
                position += 2
                column += 2
                continue
            
            # 澶勭悊鐮存姌鍙?            if line[position:position+2] == '鈥斺€?:
                tokens.append(Token(TokenType.DASH, '鈥斺€?, line_num, column, '鈥斺€?))
                position += 2
                column += 2
                continue
            
            # 澶勭悊鍦嗗湀鍙?            if line[position] in '鈶犫憽鈶⑩懀鈶も懃鈶︹懅鈶ㄢ懇':
                tokens.append(Token(TokenType.CIRCLED_NUMBERS, line[position], line_num, column, line[position]))
                position += 1
                column += 1
                continue
            
            # 澶勭悊杩愮畻绗?            if line[position] in self.operators:
                # 妫€鏌ュ弻瀛楃杩愮畻绗?                if position + 1 < len(line):
                    two_char = line[position:position+2]
                    if two_char in ('鈮?, '鈮?, '鈮?):
                        tokens.append(Token(self.operators[two_char], two_char, line_num, column, two_char))
                        position += 2
                        column += 2
                        continue
                
                tokens.append(Token(self.operators[line[position]], line[position], line_num, column, line[position]))
                position += 1
                column += 1
                continue
            
            # 澶勭悊鍒嗙粍绗﹀彿
            if line[position] in self.grouping_symbols:
                tokens.append(Token(self.grouping_symbols[line[position]], line[position], line_num, column, line[position]))
                position += 1
                column += 1
                continue
            
            # 澶勭悊瀛楃涓插瓧闈㈤噺
            if line[position] in ('"', "'"):
                string_token = self._parse_string_literal(line, position, line_num, column)
                tokens.append(string_token)
                position += len(string_token.lexeme)
                column += len(string_token.lexeme)
                continue
            
            # 澶勭悊鏁板瓧瀛楅潰閲?            if line[position].isdigit() or (line[position] == '.' and position + 1 < len(line) and line[position + 1].isdigit()):
                number_token = self._parse_number(line, position, line_num, column)
                tokens.append(number_token)
                position += len(number_token.lexeme)
                column += len(number_token.lexeme)
                continue
            
            # 澶勭悊涓枃鏁板瓧
            if line[position] in self.chinese_numbers:
                chinese_number_token = self._parse_chinese_number(line, position, line_num, column)
                tokens.append(chinese_number_token)
                position += len(chinese_number_token.lexeme)
                column += len(chinese_number_token.lexeme)
                continue
            
            # 澶勭悊褰撳墠鍒嗚瘝娈?            if segment_index < len(segments):
                segment = segments[segment_index].strip()
                if segment:  # 璺宠繃绌哄垎璇?                    # 澶勭悊鍒嗚瘝娈?                    token = self._process_segment(segment, line_num, column)
                    tokens.append(token)
                    position += len(segment)
                    column += len(segment)
                segment_index += 1
            else:
                # 濡傛灉娌℃湁鏇村鍒嗚瘝锛屽鐞嗗墿浣欏瓧绗?                identifier_token = self._parse_identifier(line, position, line_num, column)
                tokens.append(identifier_token)
                position += len(identifier_token.lexeme)
                column += len(identifier_token.lexeme)
        
        return tokens
    
    def _process_segment(self, segment: str, line_num: int, column: int) -> Token:
        """澶勭悊鍒嗚瘝娈?""
        # 妫€鏌ユ槸鍚︿负鍏抽敭璇?        token_type = self._get_keyword_type(segment)
        if token_type:
            return Token(token_type, segment, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负鐧惧濮撳彉閲?        if self._is_bai_jia_xing(segment):
            return Token(TokenType.BAIJIAXING, segment, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负鍔ㄨ瘝
        arity = get_verb_arity(segment)
        if arity != 0:
            # 鏍规嵁鍏冩暟纭畾鍔ㄨ瘝绫诲瀷
            if arity == -1:
                token_type = TokenType.VERB_VAR
            elif arity == 0:
                token_type = TokenType.VERB_0
            elif arity == 1:
                token_type = TokenType.VERB_1
            elif arity == 2:
                token_type = TokenType.VERB_2
            elif arity == 3:
                token_type = TokenType.VERB_3
            else:
                token_type = TokenType.VERB_VAR
            
            return Token(token_type, segment, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负甯冨皵瀛楅潰閲?        if segment in ('鐪?, '鍋?, 'true', 'false', 'True', 'False'):
            value = segment in ('鐪?, 'true', 'True')
            return Token(TokenType.BOOLEAN, value, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负绌哄€?        if segment == '绌?:
            return Token(TokenType.NULL, None, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负鏁板瓧
        if segment.isdigit() or (segment.replace('.', '', 1).isdigit() and segment.count('.') == 1):
            try:
                if '.' in segment:
                    value = float(segment)
                else:
                    value = int(segment)
                return Token(TokenType.NUMBER, value, line_num, column, segment)
            except ValueError:
                pass
        
        # 妫€鏌ユ槸鍚︿负涓枃鏁板瓧
        if all(c in self.chinese_numbers for c in segment):
            value = self._chinese_to_arabic(segment)
            return Token(TokenType.CHINESE_NUMBER, value, line_num, column, segment)
        
        # 鏅€氭爣璇嗙
        return Token(TokenType.IDENTIFIER, segment, line_num, column, segment)
    
    def _parse_string_literal(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽瀛楃涓插瓧闈㈤噺"""
        quote_char = line[start]
        position = start + 1
        value = ''
        
        while position < len(line):
            char = line[position]
            
            if char == quote_char:
                # 缁撴潫寮曞彿
                position += 1
                break
            elif char == '\\' and position + 1 < len(line):
                # 杞箟瀛楃
                next_char = line[position + 1]
                if next_char in ('n', 't', '\\', '"', "'"):
                    value += self._escape_char(next_char)
                    position += 2
                else:
                    value += char
                    position += 1
            else:
                value += char
                position += 1
        
        lexeme = line[start:position]
        return Token(TokenType.STRING, value, line_num, column, lexeme)
    
    def _escape_char(self, char: str) -> str:
        """杞箟瀛楃"""
        escape_map = {
            'n': '\n',
            't': '\t',
            '\\': '\\',
            '"': '"',
            "'": "'",
        }
        return escape_map.get(char, char)
    
    def _parse_number(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽鏁板瓧瀛楅潰閲?""
        position = start
        
        # 瑙ｆ瀽鏁存暟閮ㄥ垎
        while position < len(line) and line[position].isdigit():
            position += 1
        
        # 瑙ｆ瀽灏忔暟閮ㄥ垎
        if position < len(line) and line[position] == '.':
            position += 1
            while position < len(line) and line[position].isdigit():
                position += 1
        
        # 瑙ｆ瀽绉戝璁℃暟娉?        if position < len(line) and line[position].lower() == 'e':
            position += 1
            if position < len(line) and line[position] in ('+', '-'):
                position += 1
            while position < len(line) and line[position].isdigit():
                position += 1
        
        lexeme = line[start:position]
        
        # 灏濊瘯杞崲涓烘暟瀛?        try:
            if '.' in lexeme or 'e' in lexeme.lower():
                value = float(lexeme)
            else:
                value = int(lexeme)
        except ValueError:
            value = lexeme  # 淇濇寔鍘熸牱
        
        return Token(TokenType.NUMBER, value, line_num, column, lexeme)
    
    def _parse_chinese_number(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽涓枃鏁板瓧"""
        position = start
        lexeme = ''
        
        while position < len(line) and line[position] in self.chinese_numbers:
            lexeme += line[position]
            position += 1
        
        # 杞崲涓洪樋鎷変集鏁板瓧
        value = self._chinese_to_arabic(lexeme)
        
        return Token(TokenType.CHINESE_NUMBER, value, line_num, column, lexeme)
    
    def _chinese_to_arabic(self, chinese_num: str) -> int:
        """灏嗕腑鏂囨暟瀛楄浆鎹负闃挎媺浼暟瀛?""
        if not chinese_num:
            return 0
        
        # 绠€鍗曞疄鐜帮紝鍙鐞嗗熀鏈暟瀛?        total = 0
        current = 0
        
        for char in chinese_num:
            num = self.chinese_numbers.get(char, 0)
            
            if num < 10:
                current = num
            elif num >= 10:
                if current == 0:
                    current = 1
                total += current * num
                current = 0
        
        total += current
        return total
    
    def _parse_identifier(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽鏍囪瘑绗?""
        position = start
        
        # 鏀堕泦鏍囪瘑绗﹀瓧绗?        while position < len(line) and self._is_identifier_char(line[position]):
            position += 1
        
        lexeme = line[start:position]
        
        # 妫€鏌ユ槸鍚︿负鍏抽敭璇?        token_type = self._get_keyword_type(lexeme)
        if token_type:
            return Token(token_type, lexeme, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负鐧惧濮撳彉閲?        if self._is_bai_jia_xing(lexeme):
            return Token(TokenType.BAIJIAXING, lexeme, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负鍔ㄨ瘝
        arity = get_verb_arity(lexeme)
        if arity != 0:
            # 鏍规嵁鍏冩暟纭畾鍔ㄨ瘝绫诲瀷
            if arity == -1:
                token_type = TokenType.VERB_VAR
            elif arity == 0:
                token_type = TokenType.VERB_0
            elif arity == 1:
                token_type = TokenType.VERB_1
            elif arity == 2:
                token_type = TokenType.VERB_2
            elif arity == 3:
                token_type = TokenType.VERB_3
            else:
                token_type = TokenType.VERB_VAR
            
            return Token(token_type, lexeme, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负甯冨皵瀛楅潰閲?        if lexeme in ('鐪?, '鍋?, 'true', 'false', 'True', 'False'):
            value = lexeme in ('鐪?, 'true', 'True')
            return Token(TokenType.BOOLEAN, value, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负绌哄€?        if lexeme == '绌?:
            return Token(TokenType.NULL, None, line_num, column, lexeme)
        
        # 灏濊瘯涓枃鍒嗚瘝
        if len(lexeme) > 1 and any('\u4e00' <= c <= '\u9fff' for c in lexeme):
            # 浣跨敤jieba杩涜涓枃鍒嗚瘝
            segments = self._segment(lexeme)
            if len(segments) > 1:
                # 濡傛灉鏄涓瘝锛岃繑鍥炵涓€涓瘝浣滀负鏍囪瘑绗?                first_segment = segments[0]
                # 閫掑綊澶勭悊绗竴涓瘝
                return self._parse_identifier(first_segment, 0, line_num, column)
        
        # 鏅€氭爣璇嗙
        return Token(TokenType.IDENTIFIER, lexeme, line_num, column, lexeme)
    
    def _is_identifier_char(self, char: str) -> bool:
        """妫€鏌ュ瓧绗︽槸鍚︿负鏍囪瘑绗﹀瓧绗?""
        # 涓枃瀛楃銆佽嫳鏂囧瓧姣嶃€佹暟瀛椼€佷笅鍒掔嚎
        return ('\u4e00' <= char <= '\u9fff' or
                'a' <= char <= 'z' or
                'A' <= char <= 'Z' or
                char.isdigit() or
                char == '_')
    
    def _get_keyword_type(self, lexeme: str) -> Optional[TokenType]:
        """鑾峰彇鍏抽敭璇嶇被鍨?""
        # 妫€鏌ョ姸鎬佸叧閿瘝锛堝瀛楋級
        for keyword, token_type in self.state_keywords.items():
            if lexeme.startswith(keyword):
                return token_type
        
        # 妫€鏌ユ劅鐭ュ叧閿瘝锛堝瀛楋級
        for keyword, token_type in self.perception_keywords.items():
            if lexeme.startswith(keyword):
                return token_type
        
        # 妫€鏌ユ椂闂村叧閿瘝锛堝瀛楋級
        for keyword, token_type in self.time_keywords.items():
            if lexeme.startswith(keyword):
                return token_type
        
        # 妫€鏌ユ櫘閫氬叧閿瘝
        return self.keywords.get(lexeme)
    
    def _is_bai_jia_xing(self, lexeme: str) -> bool:
        """妫€鏌ユ槸鍚︿负鐧惧濮撳彉閲?""
        if not lexeme:
            return False
        
        # 鑾峰彇濮撴皬锛堢涓€涓瓧绗︼級
        surname = lexeme[0]
        
        # 妫€鏌ユ槸鍚︿负鍐茬獊濮撴皬
        if surname in self.conflict_surnames:
            return False
        
        # 妫€鏌ユ槸鍚︿负鐧惧濮?        return surname in self.bai_jia_xing
    
    def print_tokens(self, tokens: List[Token]) -> None:
        """鎵撳嵃璇嶆硶鍗曞厓鍒楄〃"""
        print("璇嶆硶鍒嗘瀽缁撴灉:")
        print("=" * 80)
        print(f"{'琛?:<4} {'鍒?:<4} {'绫诲瀷':<20} {'鍊?:<20} {'璇嶇礌':<20}")
        print("-" * 80)
        
        for token in tokens:
            value_str = str(token.value)
            if len(value_str) > 18:
                value_str = value_str[:15] + "..."
            
            lexeme_str = token.lexeme
            if len(lexeme_str) > 18:
                lexeme_str = lexeme_str[:15] + "..."
            
            print(f"{token.line:<4} {token.column:<4} {token.type.value:<20} {value_str:<20} {lexeme_str:<20}")
        
        print("=" * 80)


# 娴嬭瘯鍑芥暟
def test_lexer():
    """娴嬭瘯璇嶆硶鍒嗘瀽鍣?""
    print("璇嶆硶鍒嗘瀽鍣ㄦ祴璇?)
    print("=" * 50)
    
    lexer = YanLuLexer()
    
    # 娴嬭瘯鐢ㄤ緥
    test_cases = [
        (
            "瀹氭俯搴︽槸25銆?,
            "鍙橀噺瀹氫箟"
        ),
        (
            "濡傛灉娓╁害澶?0灏卞紑鍚鎵囥€?,
            "鏉′欢璇彞"
        ),
        (
            "瀵逛簬i鍦?鍒?0锛氬嵃i銆?,
            "寰幆璇彞"
        ),
        (
            "娓╁害鍙樹负30搴︺€?,
            "鐘舵€佽浆鎹?
        ),
        (
            "寮犱笁銆佹潕鍥涳紝璁＄畻鎶樻墸銆?,
            "鎰忓悎寮忓嚱鏁拌皟鐢?
        ),
        (
            "'浣犲ソ锛屼笘鐣?",
            "瀛楃涓插瓧闈㈤噺"
        ),
        (
            "鐪熶笖鍋?,
            "甯冨皵杩愮畻"
        ),
        (
            "瀹歺绛変簬鍗佸姞浜斻€?,
            "涓枃鏁板瓧"
        ),
    ]
    
    for source_code, description in test_cases:
        print(f"\n娴嬭瘯: {description}")
        print(f"婧愪唬鐮? {source_code}")
        
        try:
            tokens = lexer.tokenize(source_code)
            lexer.print_tokens(tokens)
        except Exception as e:
            print(f"閿欒: {e}")
    
    print("=" * 50)
    print("娴嬭瘯瀹屾垚")


if __name__ == "__main__":
    test_lexer())
    
    def _init_segmenter(self):
        """鍒濆鍖栧垎璇嶅櫒"""
        if self.segmenter_type == "thulac":
            try:
                import thulac
                # 浣跨敤seg_only=True鍙繘琛屽垎璇嶏紝涓嶈繘琛岃瘝鎬ф爣娉?                self.segmenter = thulac.thulac(seg_only=True, model_path=None)
                print(f"浣跨敤THULAC鍒嗚瘝鍣?(seg_only妯″紡)")
            except ImportError:
                print("璀﹀憡: 鏈畨瑁匱HULAC锛屽洖閫€鍒癹ieba鍒嗚瘝鍣?)
                print("瀹夎鍛戒护: pip install thulac")
                self.segmenter_type = "jieba"
                self.segmenter = jieba
        else:
            # 榛樿浣跨敤jieba
            self.segmenter = jieba
            print(f"浣跨敤jieba鍒嗚瘝鍣?)
    
    def _segment(self, text: str) -> List[str]:
        """
        鍒嗚瘝鏂规硶
        
        Args:
            text: 寰呭垎璇嶇殑鏂囨湰
            
        Returns:
            鍒嗚瘝缁撴灉鍒楄〃
        """
        if self.segmenter_type == "thulac":
            # THULAC鍒嗚瘝
            result = self.segmenter.cut(text, text=True)
            return result.split()
        else:
            # jieba鍒嗚瘝
            return list(self.segmenter.lcut(text))
        
    def tokenize(self, source_code: str) -> List[Token]:
        """
        灏嗘簮浠ｇ爜杞崲涓鸿瘝娉曞崟鍏冨垪琛?        
        Args:
            source_code: 婧愪唬鐮佸瓧绗︿覆
            
        Returns:
            璇嶆硶鍗曞厓鍒楄〃
        """
        tokens = []
        lines = source_code.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            line_tokens = self._tokenize_line(line, line_num)
            tokens.extend(line_tokens)
            
            # 娣诲姞鎹㈣绗︼紙闄ら潪鏄渶鍚庝竴琛岋級
            if line_num < len(lines):
                tokens.append(Token(TokenType.NEWLINE, '\n', line_num, len(line) + 1, '\n'))
        
        # 娣诲姞鏂囦欢缁撴潫鏍囪
        tokens.append(Token(TokenType.EOF, '', len(lines) + 1, 1, ''))
        
        return tokens
    
    def _tokenize_line(self, line: str, line_num: int) -> List[Token]:
        """灏嗕竴琛屼唬鐮佽浆鎹负璇嶆硶鍗曞厓鍒楄〃"""
        tokens = []
        position = 0
        column = 1
        
        # 浣跨敤鍒嗚瘝鍣ㄨ繘琛屼腑鏂囧垎璇?        segments = self._segment(line)
        segment_index = 0
        
        while position < len(line):
            # 璺宠繃绌虹櫧瀛楃
            if line[position].isspace():
                if line[position] == '\n':
                    tokens.append(Token(TokenType.NEWLINE, '\n', line_num, column, '\n'))
                position += 1
                column += 1
                continue
            
            # 澶勭悊娉ㄩ噴
            if line[position] == '#':
                # 鍗曡娉ㄩ噴锛岃烦杩囨暣琛?                comment = line[position:]
                tokens.append(Token(TokenType.COMMENT, comment, line_num, column, comment))
                break
            
            # 澶勭悊澶氳瑷€浠ｇ爜鍧?            if line[position:position+2] == '{{':
                tokens.append(Token(TokenType.CODE_BLOCK_START, '{{', line_num, column, '{{'))
                position += 2
                column += 2
                continue
            
            if line[position:position+2] == '}}':
                tokens.append(Token(TokenType.CODE_BLOCK_END, '}}', line_num, column, '}}'))
                position += 2
                column += 2
                continue
            
            # 澶勭悊涓枃鏍囩偣绗﹀彿
            if line[position] in self.chinese_punctuation:
                char = line[position]
                token_type = self.chinese_punctuation[char]
                
                # 澶勭悊鎴愬鏍囩偣绗﹀彿
                if char in ('銆?, '銆?):
                    # 鏌ユ壘鍖归厤鐨勭粨鏉熺鍙?                    end_pos = line.find('銆? if char == '銆? else '銆?, position + 1)
                    if end_pos != -1:
                        value = line[position:end_pos + 1]
                        tokens.append(Token(token_type, value, line_num, column, value))
                        position = end_pos + 1
                        column += len(value)
                        continue
                
                tokens.append(Token(token_type, char, line_num, column, char))
                position += 1
                column += 1
                continue
            
            # 澶勭悊鐪佺暐鍙?            if line[position:position+2] == '鈥︹€?:
                tokens.append(Token(TokenType.ELLIPSIS, '鈥︹€?, line_num, column, '鈥︹€?))
                position += 2
                column += 2
                continue
            
            # 澶勭悊鐮存姌鍙?            if line[position:position+2] == '鈥斺€?:
                tokens.append(Token(TokenType.DASH, '鈥斺€?, line_num, column, '鈥斺€?))
                position += 2
                column += 2
                continue
            
            # 澶勭悊鍦嗗湀鍙?            if line[position] in '鈶犫憽鈶⑩懀鈶も懃鈶︹懅鈶ㄢ懇':
                tokens.append(Token(TokenType.CIRCLED_NUMBERS, line[position], line_num, column, line[position]))
                position += 1
                column += 1
                continue
            
            # 澶勭悊杩愮畻绗?            if line[position] in self.operators:
                # 妫€鏌ュ弻瀛楃杩愮畻绗?                if position + 1 < len(line):
                    two_char = line[position:position+2]
                    if two_char in ('鈮?, '鈮?, '鈮?):
                        tokens.append(Token(self.operators[two_char], two_char, line_num, column, two_char))
                        position += 2
                        column += 2
                        continue
                
                tokens.append(Token(self.operators[line[position]], line[position], line_num, column, line[position]))
                position += 1
                column += 1
                continue
            
            # 澶勭悊鍒嗙粍绗﹀彿
            if line[position] in self.grouping_symbols:
                tokens.append(Token(self.grouping_symbols[line[position]], line[position], line_num, column, line[position]))
                position += 1
                column += 1
                continue
            
            # 澶勭悊瀛楃涓插瓧闈㈤噺
            if line[position] in ('"', "'"):
                string_token = self._parse_string_literal(line, position, line_num, column)
                tokens.append(string_token)
                position += len(string_token.lexeme)
                column += len(string_token.lexeme)
                continue
            
            # 澶勭悊鏁板瓧瀛楅潰閲?            if line[position].isdigit() or (line[position] == '.' and position + 1 < len(line) and line[position + 1].isdigit()):
                number_token = self._parse_number(line, position, line_num, column)
                tokens.append(number_token)
                position += len(number_token.lexeme)
                column += len(number_token.lexeme)
                continue
            
            # 澶勭悊涓枃鏁板瓧
            if line[position] in self.chinese_numbers:
                chinese_number_token = self._parse_chinese_number(line, position, line_num, column)
                tokens.append(chinese_number_token)
                position += len(chinese_number_token.lexeme)
                column += len(chinese_number_token.lexeme)
                continue
            
            # 澶勭悊褰撳墠鍒嗚瘝娈?            if segment_index < len(segments):
                segment = segments[segment_index].strip()
                if segment:  # 璺宠繃绌哄垎璇?                    # 澶勭悊鍒嗚瘝娈?                    token = self._process_segment(segment, line_num, column)
                    tokens.append(token)
                    position += len(segment)
                    column += len(segment)
                segment_index += 1
            else:
                # 濡傛灉娌℃湁鏇村鍒嗚瘝锛屽鐞嗗墿浣欏瓧绗?                identifier_token = self._parse_identifier(line, position, line_num, column)
                tokens.append(identifier_token)
                position += len(identifier_token.lexeme)
                column += len(identifier_token.lexeme)
        
        return tokens
    
    def _process_segment(self, segment: str, line_num: int, column: int) -> Token:
        """澶勭悊鍒嗚瘝娈?""
        # 妫€鏌ユ槸鍚︿负鍏抽敭璇?        token_type = self._get_keyword_type(segment)
        if token_type:
            return Token(token_type, segment, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负鐧惧濮撳彉閲?        if self._is_bai_jia_xing(segment):
            return Token(TokenType.BAIJIAXING, segment, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负鍔ㄨ瘝
        arity = get_verb_arity(segment)
        if arity != 0:
            # 鏍规嵁鍏冩暟纭畾鍔ㄨ瘝绫诲瀷
            if arity == -1:
                token_type = TokenType.VERB_VAR
            elif arity == 0:
                token_type = TokenType.VERB_0
            elif arity == 1:
                token_type = TokenType.VERB_1
            elif arity == 2:
                token_type = TokenType.VERB_2
            elif arity == 3:
                token_type = TokenType.VERB_3
            else:
                token_type = TokenType.VERB_VAR
            
            return Token(token_type, segment, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负甯冨皵瀛楅潰閲?        if segment in ('鐪?, '鍋?, 'true', 'false', 'True', 'False'):
            value = segment in ('鐪?, 'true', 'True')
            return Token(TokenType.BOOLEAN, value, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负绌哄€?        if segment == '绌?:
            return Token(TokenType.NULL, None, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负鏁板瓧
        if segment.isdigit() or (segment.replace('.', '', 1).isdigit() and segment.count('.') == 1):
            try:
                if '.' in segment:
                    value = float(segment)
                else:
                    value = int(segment)
                return Token(TokenType.NUMBER, value, line_num, column, segment)
            except ValueError:
                pass
        
        # 妫€鏌ユ槸鍚︿负涓枃鏁板瓧
        if all(c in self.chinese_numbers for c in segment):
            value = self._chinese_to_arabic(segment)
            return Token(TokenType.CHINESE_NUMBER, value, line_num, column, segment)
        
        # 鏅€氭爣璇嗙
        return Token(TokenType.IDENTIFIER, segment, line_num, column, segment)
    
    def _parse_string_literal(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽瀛楃涓插瓧闈㈤噺"""
        quote_char = line[start]
        position = start + 1
        value = ''
        
        while position < len(line):
            char = line[position]
            
            if char == quote_char:
                # 缁撴潫寮曞彿
                position += 1
                break
            elif char == '\\' and position + 1 < len(line):
                # 杞箟瀛楃
                next_char = line[position + 1]
                if next_char in ('n', 't', '\\', '"', "'"):
                    value += self._escape_char(next_char)
                    position += 2
                else:
                    value += char
                    position += 1
            else:
                value += char
                position += 1
        
        lexeme = line[start:position]
        return Token(TokenType.STRING, value, line_num, column, lexeme)
    
    def _escape_char(self, char: str) -> str:
        """杞箟瀛楃"""
        escape_map = {
            'n': '\n',
            't': '\t',
            '\\': '\\',
            '"': '"',
            "'": "'",
        }
        return escape_map.get(char, char)
    
    def _parse_number(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽鏁板瓧瀛楅潰閲?""
        position = start
        
        # 瑙ｆ瀽鏁存暟閮ㄥ垎
        while position < len(line) and line[position].isdigit():
            position += 1
        
        # 瑙ｆ瀽灏忔暟閮ㄥ垎
        if position < len(line) and line[position] == '.':
            position += 1
            while position < len(line) and line[position].isdigit():
                position += 1
        
        # 瑙ｆ瀽绉戝璁℃暟娉?        if position < len(line) and line[position].lower() == 'e':
            position += 1
            if position < len(line) and line[position] in ('+', '-'):
                position += 1
            while position < len(line) and line[position].isdigit():
                position += 1
        
        lexeme = line[start:position]
        
        # 灏濊瘯杞崲涓烘暟瀛?        try:
            if '.' in lexeme or 'e' in lexeme.lower():
                value = float(lexeme)
            else:
                value = int(lexeme)
        except ValueError:
            value = lexeme  # 淇濇寔鍘熸牱
        
        return Token(TokenType.NUMBER, value, line_num, column, lexeme)
    
    def _parse_chinese_number(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽涓枃鏁板瓧"""
        position = start
        lexeme = ''
        
        while position < len(line) and line[position] in self.chinese_numbers:
            lexeme += line[position]
            position += 1
        
        # 杞崲涓洪樋鎷変集鏁板瓧
        value = self._chinese_to_arabic(lexeme)
        
        return Token(TokenType.CHINESE_NUMBER, value, line_num, column, lexeme)
    
    def _chinese_to_arabic(self, chinese_num: str) -> int:
        """灏嗕腑鏂囨暟瀛楄浆鎹负闃挎媺浼暟瀛?""
        if not chinese_num:
            return 0
        
        # 绠€鍗曞疄鐜帮紝鍙鐞嗗熀鏈暟瀛?        total = 0
        current = 0
        
        for char in chinese_num:
            num = self.chinese_numbers.get(char, 0)
            
            if num < 10:
                current = num
            elif num >= 10:
                if current == 0:
                    current = 1
                total += current * num
                current = 0
        
        total += current
        return total
    
    def _parse_identifier(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽鏍囪瘑绗?""
        position = start
        
        # 鏀堕泦鏍囪瘑绗﹀瓧绗?        while position < len(line) and self._is_identifier_char(line[position]):
            position += 1
        
        lexeme = line[start:position]
        
        # 妫€鏌ユ槸鍚︿负鍏抽敭璇?        token_type = self._get_keyword_type(lexeme)
        if token_type:
            return Token(token_type, lexeme, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负鐧惧濮撳彉閲?        if self._is_bai_jia_xing(lexeme):
            return Token(TokenType.BAIJIAXING, lexeme, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负鍔ㄨ瘝
        arity = get_verb_arity(lexeme)
        if arity != 0:
            # 鏍规嵁鍏冩暟纭畾鍔ㄨ瘝绫诲瀷
            if arity == -1:
                token_type = TokenType.VERB_VAR
            elif arity == 0:
                token_type = TokenType.VERB_0
            elif arity == 1:
                token_type = TokenType.VERB_1
            elif arity == 2:
                token_type = TokenType.VERB_2
            elif arity == 3:
                token_type = TokenType.VERB_3
            else:
                token_type = TokenType.VERB_VAR
            
            return Token(token_type, lexeme, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负甯冨皵瀛楅潰閲?        if lexeme in ('鐪?, '鍋?, 'true', 'false', 'True', 'False'):
            value = lexeme in ('鐪?, 'true', 'True')
            return Token(TokenType.BOOLEAN, value, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负绌哄€?        if lexeme == '绌?:
            return Token(TokenType.NULL, None, line_num, column, lexeme)
        
        # 灏濊瘯涓枃鍒嗚瘝
        if len(lexeme) > 1 and any('\u4e00' <= c <= '\u9fff' for c in lexeme):
            # 浣跨敤jieba杩涜涓枃鍒嗚瘝
            segments = self._segment(lexeme)
            if len(segments) > 1:
                # 濡傛灉鏄涓瘝锛岃繑鍥炵涓€涓瘝浣滀负鏍囪瘑绗?                first_segment = segments[0]
                # 閫掑綊澶勭悊绗竴涓瘝
                return self._parse_identifier(first_segment, 0, line_num, column)
        
        # 鏅€氭爣璇嗙
        return Token(TokenType.IDENTIFIER, lexeme, line_num, column, lexeme)
    
    def _is_identifier_char(self, char: str) -> bool:
        """妫€鏌ュ瓧绗︽槸鍚︿负鏍囪瘑绗﹀瓧绗?""
        # 涓枃瀛楃銆佽嫳鏂囧瓧姣嶃€佹暟瀛椼€佷笅鍒掔嚎
        return ('\u4e00' <= char <= '\u9fff' or
                'a' <= char <= 'z' or
                'A' <= char <= 'Z' or
                char.isdigit() or
                char == '_')
    
    def _get_keyword_type(self, lexeme: str) -> Optional[TokenType]:
        """鑾峰彇鍏抽敭璇嶇被鍨?""
        # 妫€鏌ョ姸鎬佸叧閿瘝锛堝瀛楋級
        for keyword, token_type in self.state_keywords.items():
            if lexeme.startswith(keyword):
                return token_type
        
        # 妫€鏌ユ劅鐭ュ叧閿瘝锛堝瀛楋級
        for keyword, token_type in self.perception_keywords.items():
            if lexeme.startswith(keyword):
                return token_type
        
        # 妫€鏌ユ椂闂村叧閿瘝锛堝瀛楋級
        for keyword, token_type in self.time_keywords.items():
            if lexeme.startswith(keyword):
                return token_type
        
        # 妫€鏌ユ櫘閫氬叧閿瘝
        return self.keywords.get(lexeme)
    
    def _is_bai_jia_xing(self, lexeme: str) -> bool:
        """妫€鏌ユ槸鍚︿负鐧惧濮撳彉閲?""
        if not lexeme:
            return False
        
        # 鑾峰彇濮撴皬锛堢涓€涓瓧绗︼級
        surname = lexeme[0]
        
        # 妫€鏌ユ槸鍚︿负鍐茬獊濮撴皬
        if surname in self.conflict_surnames:
            return False
        
        # 妫€鏌ユ槸鍚︿负鐧惧濮?        return surname in self.bai_jia_xing
    
    def print_tokens(self, tokens: List[Token]) -> None:
        """鎵撳嵃璇嶆硶鍗曞厓鍒楄〃"""
        print("璇嶆硶鍒嗘瀽缁撴灉:")
        print("=" * 80)
        print(f"{'琛?:<4} {'鍒?:<4} {'绫诲瀷':<20} {'鍊?:<20} {'璇嶇礌':<20}")
        print("-" * 80)
        
        for token in tokens:
            value_str = str(token.value)
            if len(value_str) > 18:
                value_str = value_str[:15] + "..."
            
            lexeme_str = token.lexeme
            if len(lexeme_str) > 18:
                lexeme_str = lexeme_str[:15] + "..."
            
            print(f"{token.line:<4} {token.column:<4} {token.type.value:<20} {value_str:<20} {lexeme_str:<20}")
        
        print("=" * 80)


# 娴嬭瘯鍑芥暟
def test_lexer():
    """娴嬭瘯璇嶆硶鍒嗘瀽鍣?""
    print("璇嶆硶鍒嗘瀽鍣ㄦ祴璇?)
    print("=" * 50)
    
    lexer = YanLuLexer()
    
    # 娴嬭瘯鐢ㄤ緥
    test_cases = [
        (
            "瀹氭俯搴︽槸25銆?,
            "鍙橀噺瀹氫箟"
        ),
        (
            "濡傛灉娓╁害澶?0灏卞紑鍚鎵囥€?,
            "鏉′欢璇彞"
        ),
        (
            "瀵逛簬i鍦?鍒?0锛氬嵃i銆?,
            "寰幆璇彞"
        ),
        (
            "娓╁害鍙樹负30搴︺€?,
            "鐘舵€佽浆鎹?
        ),
        (
            "寮犱笁銆佹潕鍥涳紝璁＄畻鎶樻墸銆?,
            "鎰忓悎寮忓嚱鏁拌皟鐢?
        ),
        (
            "'浣犲ソ锛屼笘鐣?",
            "瀛楃涓插瓧闈㈤噺"
        ),
        (
            "鐪熶笖鍋?,
            "甯冨皵杩愮畻"
        ),
        (
            "瀹歺绛変簬鍗佸姞浜斻€?,
            "涓枃鏁板瓧"
        ),
    ]
    
    for source_code, description in test_cases:
        print(f"\n娴嬭瘯: {description}")
        print(f"婧愪唬鐮? {source_code}")
        
        try:
            tokens = lexer.tokenize(source_code)
            lexer.print_tokens(tokens)
        except Exception as e:
            print(f"閿欒: {e}")
    
    print("=" * 50)
    print("娴嬭瘯瀹屾垚")


if __name__ == "__main__":
    test_lexer())
        self.identifier_pattern = re.compile(r'^[\u4e00-\u9fffA-Za-z_][\u4e00-\u9fffA-Za-z0-9_]*
        """
        灏嗘簮浠ｇ爜杞崲涓鸿瘝娉曞崟鍏冨垪琛?        
        Args:
            source_code: 婧愪唬鐮佸瓧绗︿覆
            
        Returns:
            璇嶆硶鍗曞厓鍒楄〃
        """
        tokens = []
        lines = source_code.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            line_tokens = self._tokenize_line(line, line_num)
            tokens.extend(line_tokens)
            
            # 娣诲姞鎹㈣绗︼紙闄ら潪鏄渶鍚庝竴琛岋級
            if line_num < len(lines):
                tokens.append(Token(TokenType.NEWLINE, '\n', line_num, len(line) + 1, '\n'))
        
        # 娣诲姞鏂囦欢缁撴潫鏍囪
        tokens.append(Token(TokenType.EOF, '', len(lines) + 1, 1, ''))
        
        return tokens
    
    def _tokenize_line(self, line: str, line_num: int) -> List[Token]:
        """灏嗕竴琛屼唬鐮佽浆鎹负璇嶆硶鍗曞厓鍒楄〃"""
        tokens = []
        position = 0
        column = 1
        
        # 浣跨敤鍒嗚瘝鍣ㄨ繘琛屼腑鏂囧垎璇?        segments = self._segment(line)
        segment_index = 0
        
        while position < len(line):
            # 璺宠繃绌虹櫧瀛楃
            if line[position].isspace():
                if line[position] == '\n':
                    tokens.append(Token(TokenType.NEWLINE, '\n', line_num, column, '\n'))
                position += 1
                column += 1
                continue
            
            # 澶勭悊娉ㄩ噴
            if line[position] == '#':
                # 鍗曡娉ㄩ噴锛岃烦杩囨暣琛?                comment = line[position:]
                tokens.append(Token(TokenType.COMMENT, comment, line_num, column, comment))
                break
            
            # 澶勭悊澶氳瑷€浠ｇ爜鍧?            if line[position:position+2] == '{{':
                tokens.append(Token(TokenType.CODE_BLOCK_START, '{{', line_num, column, '{{'))
                position += 2
                column += 2
                continue
            
            if line[position:position+2] == '}}':
                tokens.append(Token(TokenType.CODE_BLOCK_END, '}}', line_num, column, '}}'))
                position += 2
                column += 2
                continue
            
            # 澶勭悊涓枃鏍囩偣绗﹀彿
            if line[position] in self.chinese_punctuation:
                char = line[position]
                token_type = self.chinese_punctuation[char]
                
                # 澶勭悊鎴愬鏍囩偣绗﹀彿
                if char in ('銆?, '銆?):
                    # 鏌ユ壘鍖归厤鐨勭粨鏉熺鍙?                    end_pos = line.find('銆? if char == '銆? else '銆?, position + 1)
                    if end_pos != -1:
                        value = line[position:end_pos + 1]
                        tokens.append(Token(token_type, value, line_num, column, value))
                        position = end_pos + 1
                        column += len(value)
                        continue
                
                tokens.append(Token(token_type, char, line_num, column, char))
                position += 1
                column += 1
                continue
            
            # 澶勭悊鐪佺暐鍙?            if line[position:position+2] == '鈥︹€?:
                tokens.append(Token(TokenType.ELLIPSIS, '鈥︹€?, line_num, column, '鈥︹€?))
                position += 2
                column += 2
                continue
            
            # 澶勭悊鐮存姌鍙?            if line[position:position+2] == '鈥斺€?:
                tokens.append(Token(TokenType.DASH, '鈥斺€?, line_num, column, '鈥斺€?))
                position += 2
                column += 2
                continue
            
            # 澶勭悊鍦嗗湀鍙?            if line[position] in '鈶犫憽鈶⑩懀鈶も懃鈶︹懅鈶ㄢ懇':
                tokens.append(Token(TokenType.CIRCLED_NUMBERS, line[position], line_num, column, line[position]))
                position += 1
                column += 1
                continue
            
            # 澶勭悊杩愮畻绗?            if line[position] in self.operators:
                # 妫€鏌ュ弻瀛楃杩愮畻绗?                if position + 1 < len(line):
                    two_char = line[position:position+2]
                    if two_char in ('鈮?, '鈮?, '鈮?):
                        tokens.append(Token(self.operators[two_char], two_char, line_num, column, two_char))
                        position += 2
                        column += 2
                        continue
                
                tokens.append(Token(self.operators[line[position]], line[position], line_num, column, line[position]))
                position += 1
                column += 1
                continue
            
            # 澶勭悊鍒嗙粍绗﹀彿
            if line[position] in self.grouping_symbols:
                tokens.append(Token(self.grouping_symbols[line[position]], line[position], line_num, column, line[position]))
                position += 1
                column += 1
                continue
            
            # 澶勭悊瀛楃涓插瓧闈㈤噺
            if line[position] in ('"', "'"):
                string_token = self._parse_string_literal(line, position, line_num, column)
                tokens.append(string_token)
                position += len(string_token.lexeme)
                column += len(string_token.lexeme)
                continue
            
            # 澶勭悊鏁板瓧瀛楅潰閲?            if line[position].isdigit() or (line[position] == '.' and position + 1 < len(line) and line[position + 1].isdigit()):
                number_token = self._parse_number(line, position, line_num, column)
                tokens.append(number_token)
                position += len(number_token.lexeme)
                column += len(number_token.lexeme)
                continue
            
            # 澶勭悊涓枃鏁板瓧
            if line[position] in self.chinese_numbers:
                chinese_number_token = self._parse_chinese_number(line, position, line_num, column)
                tokens.append(chinese_number_token)
                position += len(chinese_number_token.lexeme)
                column += len(chinese_number_token.lexeme)
                continue
            
            # 澶勭悊褰撳墠鍒嗚瘝娈?            if segment_index < len(segments):
                segment = segments[segment_index].strip()
                if segment:  # 璺宠繃绌哄垎璇?                    # 澶勭悊鍒嗚瘝娈?                    token = self._process_segment(segment, line_num, column)
                    tokens.append(token)
                    position += len(segment)
                    column += len(segment)
                segment_index += 1
            else:
                # 濡傛灉娌℃湁鏇村鍒嗚瘝锛屽鐞嗗墿浣欏瓧绗?                identifier_token = self._parse_identifier(line, position, line_num, column)
                tokens.append(identifier_token)
                position += len(identifier_token.lexeme)
                column += len(identifier_token.lexeme)
        
        return tokens
    
    def _process_segment(self, segment: str, line_num: int, column: int) -> Token:
        """澶勭悊鍒嗚瘝娈?""
        # 妫€鏌ユ槸鍚︿负鍏抽敭璇?        token_type = self._get_keyword_type(segment)
        if token_type:
            return Token(token_type, segment, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负鐧惧濮撳彉閲?        if self._is_bai_jia_xing(segment):
            return Token(TokenType.BAIJIAXING, segment, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负鍔ㄨ瘝
        arity = get_verb_arity(segment)
        if arity != 0:
            # 鏍规嵁鍏冩暟纭畾鍔ㄨ瘝绫诲瀷
            if arity == -1:
                token_type = TokenType.VERB_VAR
            elif arity == 0:
                token_type = TokenType.VERB_0
            elif arity == 1:
                token_type = TokenType.VERB_1
            elif arity == 2:
                token_type = TokenType.VERB_2
            elif arity == 3:
                token_type = TokenType.VERB_3
            else:
                token_type = TokenType.VERB_VAR
            
            return Token(token_type, segment, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负甯冨皵瀛楅潰閲?        if segment in ('鐪?, '鍋?, 'true', 'false', 'True', 'False'):
            value = segment in ('鐪?, 'true', 'True')
            return Token(TokenType.BOOLEAN, value, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负绌哄€?        if segment == '绌?:
            return Token(TokenType.NULL, None, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负鏁板瓧
        if segment.isdigit() or (segment.replace('.', '', 1).isdigit() and segment.count('.') == 1):
            try:
                if '.' in segment:
                    value = float(segment)
                else:
                    value = int(segment)
                return Token(TokenType.NUMBER, value, line_num, column, segment)
            except ValueError:
                pass
        
        # 妫€鏌ユ槸鍚︿负涓枃鏁板瓧
        if all(c in self.chinese_numbers for c in segment):
            value = self._chinese_to_arabic(segment)
            return Token(TokenType.CHINESE_NUMBER, value, line_num, column, segment)
        
        # 鏅€氭爣璇嗙
        return Token(TokenType.IDENTIFIER, segment, line_num, column, segment)
    
    def _parse_string_literal(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽瀛楃涓插瓧闈㈤噺"""
        quote_char = line[start]
        position = start + 1
        value = ''
        
        while position < len(line):
            char = line[position]
            
            if char == quote_char:
                # 缁撴潫寮曞彿
                position += 1
                break
            elif char == '\\' and position + 1 < len(line):
                # 杞箟瀛楃
                next_char = line[position + 1]
                if next_char in ('n', 't', '\\', '"', "'"):
                    value += self._escape_char(next_char)
                    position += 2
                else:
                    value += char
                    position += 1
            else:
                value += char
                position += 1
        
        lexeme = line[start:position]
        return Token(TokenType.STRING, value, line_num, column, lexeme)
    
    def _escape_char(self, char: str) -> str:
        """杞箟瀛楃"""
        escape_map = {
            'n': '\n',
            't': '\t',
            '\\': '\\',
            '"': '"',
            "'": "'",
        }
        return escape_map.get(char, char)
    
    def _parse_number(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽鏁板瓧瀛楅潰閲?""
        position = start
        
        # 瑙ｆ瀽鏁存暟閮ㄥ垎
        while position < len(line) and line[position].isdigit():
            position += 1
        
        # 瑙ｆ瀽灏忔暟閮ㄥ垎
        if position < len(line) and line[position] == '.':
            position += 1
            while position < len(line) and line[position].isdigit():
                position += 1
        
        # 瑙ｆ瀽绉戝璁℃暟娉?        if position < len(line) and line[position].lower() == 'e':
            position += 1
            if position < len(line) and line[position] in ('+', '-'):
                position += 1
            while position < len(line) and line[position].isdigit():
                position += 1
        
        lexeme = line[start:position]
        
        # 灏濊瘯杞崲涓烘暟瀛?        try:
            if '.' in lexeme or 'e' in lexeme.lower():
                value = float(lexeme)
            else:
                value = int(lexeme)
        except ValueError:
            value = lexeme  # 淇濇寔鍘熸牱
        
        return Token(TokenType.NUMBER, value, line_num, column, lexeme)
    
    def _parse_chinese_number(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽涓枃鏁板瓧"""
        position = start
        lexeme = ''
        
        while position < len(line) and line[position] in self.chinese_numbers:
            lexeme += line[position]
            position += 1
        
        # 杞崲涓洪樋鎷変集鏁板瓧
        value = self._chinese_to_arabic(lexeme)
        
        return Token(TokenType.CHINESE_NUMBER, value, line_num, column, lexeme)
    
    def _chinese_to_arabic(self, chinese_num: str) -> int:
        """灏嗕腑鏂囨暟瀛楄浆鎹负闃挎媺浼暟瀛?""
        if not chinese_num:
            return 0
        
        # 绠€鍗曞疄鐜帮紝鍙鐞嗗熀鏈暟瀛?        total = 0
        current = 0
        
        for char in chinese_num:
            num = self.chinese_numbers.get(char, 0)
            
            if num < 10:
                current = num
            elif num >= 10:
                if current == 0:
                    current = 1
                total += current * num
                current = 0
        
        total += current
        return total
    
    def _parse_identifier(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽鏍囪瘑绗?""
        position = start
        
        # 鏀堕泦鏍囪瘑绗﹀瓧绗?        while position < len(line) and self._is_identifier_char(line[position]):
            position += 1
        
        lexeme = line[start:position]
        
        # 妫€鏌ユ槸鍚︿负鍏抽敭璇?        token_type = self._get_keyword_type(lexeme)
        if token_type:
            return Token(token_type, lexeme, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负鐧惧濮撳彉閲?        if self._is_bai_jia_xing(lexeme):
            return Token(TokenType.BAIJIAXING, lexeme, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负鍔ㄨ瘝
        arity = get_verb_arity(lexeme)
        if arity != 0:
            # 鏍规嵁鍏冩暟纭畾鍔ㄨ瘝绫诲瀷
            if arity == -1:
                token_type = TokenType.VERB_VAR
            elif arity == 0:
                token_type = TokenType.VERB_0
            elif arity == 1:
                token_type = TokenType.VERB_1
            elif arity == 2:
                token_type = TokenType.VERB_2
            elif arity == 3:
                token_type = TokenType.VERB_3
            else:
                token_type = TokenType.VERB_VAR
            
            return Token(token_type, lexeme, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负甯冨皵瀛楅潰閲?        if lexeme in ('鐪?, '鍋?, 'true', 'false', 'True', 'False'):
            value = lexeme in ('鐪?, 'true', 'True')
            return Token(TokenType.BOOLEAN, value, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负绌哄€?        if lexeme == '绌?:
            return Token(TokenType.NULL, None, line_num, column, lexeme)
        
        # 灏濊瘯涓枃鍒嗚瘝
        if len(lexeme) > 1 and any('\u4e00' <= c <= '\u9fff' for c in lexeme):
            # 浣跨敤jieba杩涜涓枃鍒嗚瘝
            segments = self._segment(lexeme)
            if len(segments) > 1:
                # 濡傛灉鏄涓瘝锛岃繑鍥炵涓€涓瘝浣滀负鏍囪瘑绗?                first_segment = segments[0]
                # 閫掑綊澶勭悊绗竴涓瘝
                return self._parse_identifier(first_segment, 0, line_num, column)
        
        # 鏅€氭爣璇嗙
        return Token(TokenType.IDENTIFIER, lexeme, line_num, column, lexeme)
    
    def _is_identifier_char(self, char: str) -> bool:
        """妫€鏌ュ瓧绗︽槸鍚︿负鏍囪瘑绗﹀瓧绗?""
        # 涓枃瀛楃銆佽嫳鏂囧瓧姣嶃€佹暟瀛椼€佷笅鍒掔嚎
        return ('\u4e00' <= char <= '\u9fff' or
                'a' <= char <= 'z' or
                'A' <= char <= 'Z' or
                char.isdigit() or
                char == '_')
    
    def _get_keyword_type(self, lexeme: str) -> Optional[TokenType]:
        """鑾峰彇鍏抽敭璇嶇被鍨?""
        # 妫€鏌ョ姸鎬佸叧閿瘝锛堝瀛楋級
        for keyword, token_type in self.state_keywords.items():
            if lexeme.startswith(keyword):
                return token_type
        
        # 妫€鏌ユ劅鐭ュ叧閿瘝锛堝瀛楋級
        for keyword, token_type in self.perception_keywords.items():
            if lexeme.startswith(keyword):
                return token_type
        
        # 妫€鏌ユ椂闂村叧閿瘝锛堝瀛楋級
        for keyword, token_type in self.time_keywords.items():
            if lexeme.startswith(keyword):
                return token_type
        
        # 妫€鏌ユ櫘閫氬叧閿瘝
        return self.keywords.get(lexeme)
    
    def _is_bai_jia_xing(self, lexeme: str) -> bool:
        """妫€鏌ユ槸鍚︿负鐧惧濮撳彉閲?""
        if not lexeme:
            return False
        
        # 鑾峰彇濮撴皬锛堢涓€涓瓧绗︼級
        surname = lexeme[0]
        
        # 妫€鏌ユ槸鍚︿负鍐茬獊濮撴皬
        if surname in self.conflict_surnames:
            return False
        
        # 妫€鏌ユ槸鍚︿负鐧惧濮?        return surname in self.bai_jia_xing
    
    def print_tokens(self, tokens: List[Token]) -> None:
        """鎵撳嵃璇嶆硶鍗曞厓鍒楄〃"""
        print("璇嶆硶鍒嗘瀽缁撴灉:")
        print("=" * 80)
        print(f"{'琛?:<4} {'鍒?:<4} {'绫诲瀷':<20} {'鍊?:<20} {'璇嶇礌':<20}")
        print("-" * 80)
        
        for token in tokens:
            value_str = str(token.value)
            if len(value_str) > 18:
                value_str = value_str[:15] + "..."
            
            lexeme_str = token.lexeme
            if len(lexeme_str) > 18:
                lexeme_str = lexeme_str[:15] + "..."
            
            print(f"{token.line:<4} {token.column:<4} {token.type.value:<20} {value_str:<20} {lexeme_str:<20}")
        
        print("=" * 80)


# 娴嬭瘯鍑芥暟
def test_lexer():
    """娴嬭瘯璇嶆硶鍒嗘瀽鍣?""
    print("璇嶆硶鍒嗘瀽鍣ㄦ祴璇?)
    print("=" * 50)
    
    lexer = YanLuLexer()
    
    # 娴嬭瘯鐢ㄤ緥
    test_cases = [
        (
            "瀹氭俯搴︽槸25銆?,
            "鍙橀噺瀹氫箟"
        ),
        (
            "濡傛灉娓╁害澶?0灏卞紑鍚鎵囥€?,
            "鏉′欢璇彞"
        ),
        (
            "瀵逛簬i鍦?鍒?0锛氬嵃i銆?,
            "寰幆璇彞"
        ),
        (
            "娓╁害鍙樹负30搴︺€?,
            "鐘舵€佽浆鎹?
        ),
        (
            "寮犱笁銆佹潕鍥涳紝璁＄畻鎶樻墸銆?,
            "鎰忓悎寮忓嚱鏁拌皟鐢?
        ),
        (
            "'浣犲ソ锛屼笘鐣?",
            "瀛楃涓插瓧闈㈤噺"
        ),
        (
            "鐪熶笖鍋?,
            "甯冨皵杩愮畻"
        ),
        (
            "瀹歺绛変簬鍗佸姞浜斻€?,
            "涓枃鏁板瓧"
        ),
    ]
    
    for source_code, description in test_cases:
        print(f"\n娴嬭瘯: {description}")
        print(f"婧愪唬鐮? {source_code}")
        
        try:
            tokens = lexer.tokenize(source_code)
            lexer.print_tokens(tokens)
        except Exception as e:
            print(f"閿欒: {e}")
    
    print("=" * 50)
    print("娴嬭瘯瀹屾垚")


if __name__ == "__main__":
    test_lexer())
    
    def _init_segmenter(self):
        """鍒濆鍖栧垎璇嶅櫒"""
        if self.segmenter_type == "thulac":
            try:
                import thulac
                # 浣跨敤seg_only=True鍙繘琛屽垎璇嶏紝涓嶈繘琛岃瘝鎬ф爣娉?                self.segmenter = thulac.thulac(seg_only=True, model_path=None)
                print(f"浣跨敤THULAC鍒嗚瘝鍣?(seg_only妯″紡)")
            except ImportError:
                print("璀﹀憡: 鏈畨瑁匱HULAC锛屽洖閫€鍒癹ieba鍒嗚瘝鍣?)
                print("瀹夎鍛戒护: pip install thulac")
                self.segmenter_type = "jieba"
                self.segmenter = jieba
        else:
            # 榛樿浣跨敤jieba
            self.segmenter = jieba
            print(f"浣跨敤jieba鍒嗚瘝鍣?)
    
    def _segment(self, text: str) -> List[str]:
        """
        鍒嗚瘝鏂规硶
        
        Args:
            text: 寰呭垎璇嶇殑鏂囨湰
            
        Returns:
            鍒嗚瘝缁撴灉鍒楄〃
        """
        if self.segmenter_type == "thulac":
            # THULAC鍒嗚瘝
            result = self.segmenter.cut(text, text=True)
            return result.split()
        else:
            # jieba鍒嗚瘝
            return list(self.segmenter.lcut(text))
        
    def tokenize(self, source_code: str) -> List[Token]:
        """
        灏嗘簮浠ｇ爜杞崲涓鸿瘝娉曞崟鍏冨垪琛?        
        Args:
            source_code: 婧愪唬鐮佸瓧绗︿覆
            
        Returns:
            璇嶆硶鍗曞厓鍒楄〃
        """
        tokens = []
        lines = source_code.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            line_tokens = self._tokenize_line(line, line_num)
            tokens.extend(line_tokens)
            
            # 娣诲姞鎹㈣绗︼紙闄ら潪鏄渶鍚庝竴琛岋級
            if line_num < len(lines):
                tokens.append(Token(TokenType.NEWLINE, '\n', line_num, len(line) + 1, '\n'))
        
        # 娣诲姞鏂囦欢缁撴潫鏍囪
        tokens.append(Token(TokenType.EOF, '', len(lines) + 1, 1, ''))
        
        return tokens
    
    def _tokenize_line(self, line: str, line_num: int) -> List[Token]:
        """灏嗕竴琛屼唬鐮佽浆鎹负璇嶆硶鍗曞厓鍒楄〃"""
        tokens = []
        position = 0
        column = 1
        
        # 浣跨敤鍒嗚瘝鍣ㄨ繘琛屼腑鏂囧垎璇?        segments = self._segment(line)
        segment_index = 0
        
        while position < len(line):
            # 璺宠繃绌虹櫧瀛楃
            if line[position].isspace():
                if line[position] == '\n':
                    tokens.append(Token(TokenType.NEWLINE, '\n', line_num, column, '\n'))
                position += 1
                column += 1
                continue
            
            # 澶勭悊娉ㄩ噴
            if line[position] == '#':
                # 鍗曡娉ㄩ噴锛岃烦杩囨暣琛?                comment = line[position:]
                tokens.append(Token(TokenType.COMMENT, comment, line_num, column, comment))
                break
            
            # 澶勭悊澶氳瑷€浠ｇ爜鍧?            if line[position:position+2] == '{{':
                tokens.append(Token(TokenType.CODE_BLOCK_START, '{{', line_num, column, '{{'))
                position += 2
                column += 2
                continue
            
            if line[position:position+2] == '}}':
                tokens.append(Token(TokenType.CODE_BLOCK_END, '}}', line_num, column, '}}'))
                position += 2
                column += 2
                continue
            
            # 澶勭悊涓枃鏍囩偣绗﹀彿
            if line[position] in self.chinese_punctuation:
                char = line[position]
                token_type = self.chinese_punctuation[char]
                
                # 澶勭悊鎴愬鏍囩偣绗﹀彿
                if char in ('銆?, '銆?):
                    # 鏌ユ壘鍖归厤鐨勭粨鏉熺鍙?                    end_pos = line.find('銆? if char == '銆? else '銆?, position + 1)
                    if end_pos != -1:
                        value = line[position:end_pos + 1]
                        tokens.append(Token(token_type, value, line_num, column, value))
                        position = end_pos + 1
                        column += len(value)
                        continue
                
                tokens.append(Token(token_type, char, line_num, column, char))
                position += 1
                column += 1
                continue
            
            # 澶勭悊鐪佺暐鍙?            if line[position:position+2] == '鈥︹€?:
                tokens.append(Token(TokenType.ELLIPSIS, '鈥︹€?, line_num, column, '鈥︹€?))
                position += 2
                column += 2
                continue
            
            # 澶勭悊鐮存姌鍙?            if line[position:position+2] == '鈥斺€?:
                tokens.append(Token(TokenType.DASH, '鈥斺€?, line_num, column, '鈥斺€?))
                position += 2
                column += 2
                continue
            
            # 澶勭悊鍦嗗湀鍙?            if line[position] in '鈶犫憽鈶⑩懀鈶も懃鈶︹懅鈶ㄢ懇':
                tokens.append(Token(TokenType.CIRCLED_NUMBERS, line[position], line_num, column, line[position]))
                position += 1
                column += 1
                continue
            
            # 澶勭悊杩愮畻绗?            if line[position] in self.operators:
                # 妫€鏌ュ弻瀛楃杩愮畻绗?                if position + 1 < len(line):
                    two_char = line[position:position+2]
                    if two_char in ('鈮?, '鈮?, '鈮?):
                        tokens.append(Token(self.operators[two_char], two_char, line_num, column, two_char))
                        position += 2
                        column += 2
                        continue
                
                tokens.append(Token(self.operators[line[position]], line[position], line_num, column, line[position]))
                position += 1
                column += 1
                continue
            
            # 澶勭悊鍒嗙粍绗﹀彿
            if line[position] in self.grouping_symbols:
                tokens.append(Token(self.grouping_symbols[line[position]], line[position], line_num, column, line[position]))
                position += 1
                column += 1
                continue
            
            # 澶勭悊瀛楃涓插瓧闈㈤噺
            if line[position] in ('"', "'"):
                string_token = self._parse_string_literal(line, position, line_num, column)
                tokens.append(string_token)
                position += len(string_token.lexeme)
                column += len(string_token.lexeme)
                continue
            
            # 澶勭悊鏁板瓧瀛楅潰閲?            if line[position].isdigit() or (line[position] == '.' and position + 1 < len(line) and line[position + 1].isdigit()):
                number_token = self._parse_number(line, position, line_num, column)
                tokens.append(number_token)
                position += len(number_token.lexeme)
                column += len(number_token.lexeme)
                continue
            
            # 澶勭悊涓枃鏁板瓧
            if line[position] in self.chinese_numbers:
                chinese_number_token = self._parse_chinese_number(line, position, line_num, column)
                tokens.append(chinese_number_token)
                position += len(chinese_number_token.lexeme)
                column += len(chinese_number_token.lexeme)
                continue
            
            # 澶勭悊褰撳墠鍒嗚瘝娈?            if segment_index < len(segments):
                segment = segments[segment_index].strip()
                if segment:  # 璺宠繃绌哄垎璇?                    # 澶勭悊鍒嗚瘝娈?                    token = self._process_segment(segment, line_num, column)
                    tokens.append(token)
                    position += len(segment)
                    column += len(segment)
                segment_index += 1
            else:
                # 濡傛灉娌℃湁鏇村鍒嗚瘝锛屽鐞嗗墿浣欏瓧绗?                identifier_token = self._parse_identifier(line, position, line_num, column)
                tokens.append(identifier_token)
                position += len(identifier_token.lexeme)
                column += len(identifier_token.lexeme)
        
        return tokens
    
    def _process_segment(self, segment: str, line_num: int, column: int) -> Token:
        """澶勭悊鍒嗚瘝娈?""
        # 妫€鏌ユ槸鍚︿负鍏抽敭璇?        token_type = self._get_keyword_type(segment)
        if token_type:
            return Token(token_type, segment, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负鐧惧濮撳彉閲?        if self._is_bai_jia_xing(segment):
            return Token(TokenType.BAIJIAXING, segment, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负鍔ㄨ瘝
        arity = get_verb_arity(segment)
        if arity != 0:
            # 鏍规嵁鍏冩暟纭畾鍔ㄨ瘝绫诲瀷
            if arity == -1:
                token_type = TokenType.VERB_VAR
            elif arity == 0:
                token_type = TokenType.VERB_0
            elif arity == 1:
                token_type = TokenType.VERB_1
            elif arity == 2:
                token_type = TokenType.VERB_2
            elif arity == 3:
                token_type = TokenType.VERB_3
            else:
                token_type = TokenType.VERB_VAR
            
            return Token(token_type, segment, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负甯冨皵瀛楅潰閲?        if segment in ('鐪?, '鍋?, 'true', 'false', 'True', 'False'):
            value = segment in ('鐪?, 'true', 'True')
            return Token(TokenType.BOOLEAN, value, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负绌哄€?        if segment == '绌?:
            return Token(TokenType.NULL, None, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负鏁板瓧
        if segment.isdigit() or (segment.replace('.', '', 1).isdigit() and segment.count('.') == 1):
            try:
                if '.' in segment:
                    value = float(segment)
                else:
                    value = int(segment)
                return Token(TokenType.NUMBER, value, line_num, column, segment)
            except ValueError:
                pass
        
        # 妫€鏌ユ槸鍚︿负涓枃鏁板瓧
        if all(c in self.chinese_numbers for c in segment):
            value = self._chinese_to_arabic(segment)
            return Token(TokenType.CHINESE_NUMBER, value, line_num, column, segment)
        
        # 鏅€氭爣璇嗙
        return Token(TokenType.IDENTIFIER, segment, line_num, column, segment)
    
    def _parse_string_literal(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽瀛楃涓插瓧闈㈤噺"""
        quote_char = line[start]
        position = start + 1
        value = ''
        
        while position < len(line):
            char = line[position]
            
            if char == quote_char:
                # 缁撴潫寮曞彿
                position += 1
                break
            elif char == '\\' and position + 1 < len(line):
                # 杞箟瀛楃
                next_char = line[position + 1]
                if next_char in ('n', 't', '\\', '"', "'"):
                    value += self._escape_char(next_char)
                    position += 2
                else:
                    value += char
                    position += 1
            else:
                value += char
                position += 1
        
        lexeme = line[start:position]
        return Token(TokenType.STRING, value, line_num, column, lexeme)
    
    def _escape_char(self, char: str) -> str:
        """杞箟瀛楃"""
        escape_map = {
            'n': '\n',
            't': '\t',
            '\\': '\\',
            '"': '"',
            "'": "'",
        }
        return escape_map.get(char, char)
    
    def _parse_number(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽鏁板瓧瀛楅潰閲?""
        position = start
        
        # 瑙ｆ瀽鏁存暟閮ㄥ垎
        while position < len(line) and line[position].isdigit():
            position += 1
        
        # 瑙ｆ瀽灏忔暟閮ㄥ垎
        if position < len(line) and line[position] == '.':
            position += 1
            while position < len(line) and line[position].isdigit():
                position += 1
        
        # 瑙ｆ瀽绉戝璁℃暟娉?        if position < len(line) and line[position].lower() == 'e':
            position += 1
            if position < len(line) and line[position] in ('+', '-'):
                position += 1
            while position < len(line) and line[position].isdigit():
                position += 1
        
        lexeme = line[start:position]
        
        # 灏濊瘯杞崲涓烘暟瀛?        try:
            if '.' in lexeme or 'e' in lexeme.lower():
                value = float(lexeme)
            else:
                value = int(lexeme)
        except ValueError:
            value = lexeme  # 淇濇寔鍘熸牱
        
        return Token(TokenType.NUMBER, value, line_num, column, lexeme)
    
    def _parse_chinese_number(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽涓枃鏁板瓧"""
        position = start
        lexeme = ''
        
        while position < len(line) and line[position] in self.chinese_numbers:
            lexeme += line[position]
            position += 1
        
        # 杞崲涓洪樋鎷変集鏁板瓧
        value = self._chinese_to_arabic(lexeme)
        
        return Token(TokenType.CHINESE_NUMBER, value, line_num, column, lexeme)
    
    def _chinese_to_arabic(self, chinese_num: str) -> int:
        """灏嗕腑鏂囨暟瀛楄浆鎹负闃挎媺浼暟瀛?""
        if not chinese_num:
            return 0
        
        # 绠€鍗曞疄鐜帮紝鍙鐞嗗熀鏈暟瀛?        total = 0
        current = 0
        
        for char in chinese_num:
            num = self.chinese_numbers.get(char, 0)
            
            if num < 10:
                current = num
            elif num >= 10:
                if current == 0:
                    current = 1
                total += current * num
                current = 0
        
        total += current
        return total
    
    def _parse_identifier(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽鏍囪瘑绗?""
        position = start
        
        # 鏀堕泦鏍囪瘑绗﹀瓧绗?        while position < len(line) and self._is_identifier_char(line[position]):
            position += 1
        
        lexeme = line[start:position]
        
        # 妫€鏌ユ槸鍚︿负鍏抽敭璇?        token_type = self._get_keyword_type(lexeme)
        if token_type:
            return Token(token_type, lexeme, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负鐧惧濮撳彉閲?        if self._is_bai_jia_xing(lexeme):
            return Token(TokenType.BAIJIAXING, lexeme, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负鍔ㄨ瘝
        arity = get_verb_arity(lexeme)
        if arity != 0:
            # 鏍规嵁鍏冩暟纭畾鍔ㄨ瘝绫诲瀷
            if arity == -1:
                token_type = TokenType.VERB_VAR
            elif arity == 0:
                token_type = TokenType.VERB_0
            elif arity == 1:
                token_type = TokenType.VERB_1
            elif arity == 2:
                token_type = TokenType.VERB_2
            elif arity == 3:
                token_type = TokenType.VERB_3
            else:
                token_type = TokenType.VERB_VAR
            
            return Token(token_type, lexeme, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负甯冨皵瀛楅潰閲?        if lexeme in ('鐪?, '鍋?, 'true', 'false', 'True', 'False'):
            value = lexeme in ('鐪?, 'true', 'True')
            return Token(TokenType.BOOLEAN, value, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负绌哄€?        if lexeme == '绌?:
            return Token(TokenType.NULL, None, line_num, column, lexeme)
        
        # 灏濊瘯涓枃鍒嗚瘝
        if len(lexeme) > 1 and any('\u4e00' <= c <= '\u9fff' for c in lexeme):
            # 浣跨敤jieba杩涜涓枃鍒嗚瘝
            segments = self._segment(lexeme)
            if len(segments) > 1:
                # 濡傛灉鏄涓瘝锛岃繑鍥炵涓€涓瘝浣滀负鏍囪瘑绗?                first_segment = segments[0]
                # 閫掑綊澶勭悊绗竴涓瘝
                return self._parse_identifier(first_segment, 0, line_num, column)
        
        # 鏅€氭爣璇嗙
        return Token(TokenType.IDENTIFIER, lexeme, line_num, column, lexeme)
    
    def _is_identifier_char(self, char: str) -> bool:
        """妫€鏌ュ瓧绗︽槸鍚︿负鏍囪瘑绗﹀瓧绗?""
        # 涓枃瀛楃銆佽嫳鏂囧瓧姣嶃€佹暟瀛椼€佷笅鍒掔嚎
        return ('\u4e00' <= char <= '\u9fff' or
                'a' <= char <= 'z' or
                'A' <= char <= 'Z' or
                char.isdigit() or
                char == '_')
    
    def _get_keyword_type(self, lexeme: str) -> Optional[TokenType]:
        """鑾峰彇鍏抽敭璇嶇被鍨?""
        # 妫€鏌ョ姸鎬佸叧閿瘝锛堝瀛楋級
        for keyword, token_type in self.state_keywords.items():
            if lexeme.startswith(keyword):
                return token_type
        
        # 妫€鏌ユ劅鐭ュ叧閿瘝锛堝瀛楋級
        for keyword, token_type in self.perception_keywords.items():
            if lexeme.startswith(keyword):
                return token_type
        
        # 妫€鏌ユ椂闂村叧閿瘝锛堝瀛楋級
        for keyword, token_type in self.time_keywords.items():
            if lexeme.startswith(keyword):
                return token_type
        
        # 妫€鏌ユ櫘閫氬叧閿瘝
        return self.keywords.get(lexeme)
    
    def _is_bai_jia_xing(self, lexeme: str) -> bool:
        """妫€鏌ユ槸鍚︿负鐧惧濮撳彉閲?""
        if not lexeme:
            return False
        
        # 鑾峰彇濮撴皬锛堢涓€涓瓧绗︼級
        surname = lexeme[0]
        
        # 妫€鏌ユ槸鍚︿负鍐茬獊濮撴皬
        if surname in self.conflict_surnames:
            return False
        
        # 妫€鏌ユ槸鍚︿负鐧惧濮?        return surname in self.bai_jia_xing
    
    def print_tokens(self, tokens: List[Token]) -> None:
        """鎵撳嵃璇嶆硶鍗曞厓鍒楄〃"""
        print("璇嶆硶鍒嗘瀽缁撴灉:")
        print("=" * 80)
        print(f"{'琛?:<4} {'鍒?:<4} {'绫诲瀷':<20} {'鍊?:<20} {'璇嶇礌':<20}")
        print("-" * 80)
        
        for token in tokens:
            value_str = str(token.value)
            if len(value_str) > 18:
                value_str = value_str[:15] + "..."
            
            lexeme_str = token.lexeme
            if len(lexeme_str) > 18:
                lexeme_str = lexeme_str[:15] + "..."
            
            print(f"{token.line:<4} {token.column:<4} {token.type.value:<20} {value_str:<20} {lexeme_str:<20}")
        
        print("=" * 80)


# 娴嬭瘯鍑芥暟
def test_lexer():
    """娴嬭瘯璇嶆硶鍒嗘瀽鍣?""
    print("璇嶆硶鍒嗘瀽鍣ㄦ祴璇?)
    print("=" * 50)
    
    lexer = YanLuLexer()
    
    # 娴嬭瘯鐢ㄤ緥
    test_cases = [
        (
            "瀹氭俯搴︽槸25銆?,
            "鍙橀噺瀹氫箟"
        ),
        (
            "濡傛灉娓╁害澶?0灏卞紑鍚鎵囥€?,
            "鏉′欢璇彞"
        ),
        (
            "瀵逛簬i鍦?鍒?0锛氬嵃i銆?,
            "寰幆璇彞"
        ),
        (
            "娓╁害鍙樹负30搴︺€?,
            "鐘舵€佽浆鎹?
        ),
        (
            "寮犱笁銆佹潕鍥涳紝璁＄畻鎶樻墸銆?,
            "鎰忓悎寮忓嚱鏁拌皟鐢?
        ),
        (
            "'浣犲ソ锛屼笘鐣?",
            "瀛楃涓插瓧闈㈤噺"
        ),
        (
            "鐪熶笖鍋?,
            "甯冨皵杩愮畻"
        ),
        (
            "瀹歺绛変簬鍗佸姞浜斻€?,
            "涓枃鏁板瓧"
        ),
    ]
    
    for source_code, description in test_cases:
        print(f"\n娴嬭瘯: {description}")
        print(f"婧愪唬鐮? {source_code}")
        
        try:
            tokens = lexer.tokenize(source_code)
            lexer.print_tokens(tokens)
        except Exception as e:
            print(f"閿欒: {e}")
    
    print("=" * 50)
    print("娴嬭瘯瀹屾垚")


if __name__ == "__main__":
    test_lexer())
        self.identifier_pattern = re.compile(r'^[\u4e00-\u9fffA-Za-z_][\u4e00-\u9fffA-Za-z0-9_]*
        
        Args:
            source_code: 婧愪唬鐮佸瓧绗︿覆
            
        Returns:
            璇嶆硶鍗曞厓鍒楄〃
        """
        tokens = []
        lines = source_code.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            line_tokens = self._tokenize_line(line, line_num)
            tokens.extend(line_tokens)
            
            # 娣诲姞鎹㈣绗︼紙闄ら潪鏄渶鍚庝竴琛岋級
            if line_num < len(lines):
                tokens.append(Token(TokenType.NEWLINE, '\n', line_num, len(line) + 1, '\n'))
        
        # 娣诲姞鏂囦欢缁撴潫鏍囪
        tokens.append(Token(TokenType.EOF, '', len(lines) + 1, 1, ''))
        
        return tokens
    
    def _tokenize_line(self, line: str, line_num: int) -> List[Token]:
        """灏嗕竴琛屼唬鐮佽浆鎹负璇嶆硶鍗曞厓鍒楄〃"""
        tokens = []
        position = 0
        column = 1
        
        # 浣跨敤鍒嗚瘝鍣ㄨ繘琛屼腑鏂囧垎璇?        segments = self._segment(line)
        segment_index = 0
        
        while position < len(line):
            # 璺宠繃绌虹櫧瀛楃
            if line[position].isspace():
                if line[position] == '\n':
                    tokens.append(Token(TokenType.NEWLINE, '\n', line_num, column, '\n'))
                position += 1
                column += 1
                continue
            
            # 澶勭悊娉ㄩ噴
            if line[position] == '#':
                # 鍗曡娉ㄩ噴锛岃烦杩囨暣琛?                comment = line[position:]
                tokens.append(Token(TokenType.COMMENT, comment, line_num, column, comment))
                break
            
            # 澶勭悊澶氳瑷€浠ｇ爜鍧?            if line[position:position+2] == '{{':
                tokens.append(Token(TokenType.CODE_BLOCK_START, '{{', line_num, column, '{{'))
                position += 2
                column += 2
                continue
            
            if line[position:position+2] == '}}':
                tokens.append(Token(TokenType.CODE_BLOCK_END, '}}', line_num, column, '}}'))
                position += 2
                column += 2
                continue
            
            # 澶勭悊涓枃鏍囩偣绗﹀彿
            if line[position] in self.chinese_punctuation:
                char = line[position]
                token_type = self.chinese_punctuation[char]
                
                # 澶勭悊鎴愬鏍囩偣绗﹀彿
                if char in ('銆?, '銆?):
                    # 鏌ユ壘鍖归厤鐨勭粨鏉熺鍙?                    end_pos = line.find('銆? if char == '銆? else '銆?, position + 1)
                    if end_pos != -1:
                        value = line[position:end_pos + 1]
                        tokens.append(Token(token_type, value, line_num, column, value))
                        position = end_pos + 1
                        column += len(value)
                        continue
                
                tokens.append(Token(token_type, char, line_num, column, char))
                position += 1
                column += 1
                continue
            
            # 澶勭悊鐪佺暐鍙?            if line[position:position+2] == '鈥︹€?:
                tokens.append(Token(TokenType.ELLIPSIS, '鈥︹€?, line_num, column, '鈥︹€?))
                position += 2
                column += 2
                continue
            
            # 澶勭悊鐮存姌鍙?            if line[position:position+2] == '鈥斺€?:
                tokens.append(Token(TokenType.DASH, '鈥斺€?, line_num, column, '鈥斺€?))
                position += 2
                column += 2
                continue
            
            # 澶勭悊鍦嗗湀鍙?            if line[position] in '鈶犫憽鈶⑩懀鈶も懃鈶︹懅鈶ㄢ懇':
                tokens.append(Token(TokenType.CIRCLED_NUMBERS, line[position], line_num, column, line[position]))
                position += 1
                column += 1
                continue
            
            # 澶勭悊杩愮畻绗?            if line[position] in self.operators:
                # 妫€鏌ュ弻瀛楃杩愮畻绗?                if position + 1 < len(line):
                    two_char = line[position:position+2]
                    if two_char in ('鈮?, '鈮?, '鈮?):
                        tokens.append(Token(self.operators[two_char], two_char, line_num, column, two_char))
                        position += 2
                        column += 2
                        continue
                
                tokens.append(Token(self.operators[line[position]], line[position], line_num, column, line[position]))
                position += 1
                column += 1
                continue
            
            # 澶勭悊鍒嗙粍绗﹀彿
            if line[position] in self.grouping_symbols:
                tokens.append(Token(self.grouping_symbols[line[position]], line[position], line_num, column, line[position]))
                position += 1
                column += 1
                continue
            
            # 澶勭悊瀛楃涓插瓧闈㈤噺
            if line[position] in ('"', "'"):
                string_token = self._parse_string_literal(line, position, line_num, column)
                tokens.append(string_token)
                position += len(string_token.lexeme)
                column += len(string_token.lexeme)
                continue
            
            # 澶勭悊鏁板瓧瀛楅潰閲?            if line[position].isdigit() or (line[position] == '.' and position + 1 < len(line) and line[position + 1].isdigit()):
                number_token = self._parse_number(line, position, line_num, column)
                tokens.append(number_token)
                position += len(number_token.lexeme)
                column += len(number_token.lexeme)
                continue
            
            # 澶勭悊涓枃鏁板瓧
            if line[position] in self.chinese_numbers:
                chinese_number_token = self._parse_chinese_number(line, position, line_num, column)
                tokens.append(chinese_number_token)
                position += len(chinese_number_token.lexeme)
                column += len(chinese_number_token.lexeme)
                continue
            
            # 澶勭悊褰撳墠鍒嗚瘝娈?            if segment_index < len(segments):
                segment = segments[segment_index].strip()
                if segment:  # 璺宠繃绌哄垎璇?                    # 澶勭悊鍒嗚瘝娈?                    token = self._process_segment(segment, line_num, column)
                    tokens.append(token)
                    position += len(segment)
                    column += len(segment)
                segment_index += 1
            else:
                # 濡傛灉娌℃湁鏇村鍒嗚瘝锛屽鐞嗗墿浣欏瓧绗?                identifier_token = self._parse_identifier(line, position, line_num, column)
                tokens.append(identifier_token)
                position += len(identifier_token.lexeme)
                column += len(identifier_token.lexeme)
        
        return tokens
    
    def _process_segment(self, segment: str, line_num: int, column: int) -> Token:
        """澶勭悊鍒嗚瘝娈?""
        # 妫€鏌ユ槸鍚︿负鍏抽敭璇?        token_type = self._get_keyword_type(segment)
        if token_type:
            return Token(token_type, segment, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负鐧惧濮撳彉閲?        if self._is_bai_jia_xing(segment):
            return Token(TokenType.BAIJIAXING, segment, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负鍔ㄨ瘝
        arity = get_verb_arity(segment)
        if arity != 0:
            # 鏍规嵁鍏冩暟纭畾鍔ㄨ瘝绫诲瀷
            if arity == -1:
                token_type = TokenType.VERB_VAR
            elif arity == 0:
                token_type = TokenType.VERB_0
            elif arity == 1:
                token_type = TokenType.VERB_1
            elif arity == 2:
                token_type = TokenType.VERB_2
            elif arity == 3:
                token_type = TokenType.VERB_3
            else:
                token_type = TokenType.VERB_VAR
            
            return Token(token_type, segment, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负甯冨皵瀛楅潰閲?        if segment in ('鐪?, '鍋?, 'true', 'false', 'True', 'False'):
            value = segment in ('鐪?, 'true', 'True')
            return Token(TokenType.BOOLEAN, value, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负绌哄€?        if segment == '绌?:
            return Token(TokenType.NULL, None, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负鏁板瓧
        if segment.isdigit() or (segment.replace('.', '', 1).isdigit() and segment.count('.') == 1):
            try:
                if '.' in segment:
                    value = float(segment)
                else:
                    value = int(segment)
                return Token(TokenType.NUMBER, value, line_num, column, segment)
            except ValueError:
                pass
        
        # 妫€鏌ユ槸鍚︿负涓枃鏁板瓧
        if all(c in self.chinese_numbers for c in segment):
            value = self._chinese_to_arabic(segment)
            return Token(TokenType.CHINESE_NUMBER, value, line_num, column, segment)
        
        # 鏅€氭爣璇嗙
        return Token(TokenType.IDENTIFIER, segment, line_num, column, segment)
    
    def _parse_string_literal(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽瀛楃涓插瓧闈㈤噺"""
        quote_char = line[start]
        position = start + 1
        value = ''
        
        while position < len(line):
            char = line[position]
            
            if char == quote_char:
                # 缁撴潫寮曞彿
                position += 1
                break
            elif char == '\\' and position + 1 < len(line):
                # 杞箟瀛楃
                next_char = line[position + 1]
                if next_char in ('n', 't', '\\', '"', "'"):
                    value += self._escape_char(next_char)
                    position += 2
                else:
                    value += char
                    position += 1
            else:
                value += char
                position += 1
        
        lexeme = line[start:position]
        return Token(TokenType.STRING, value, line_num, column, lexeme)
    
    def _escape_char(self, char: str) -> str:
        """杞箟瀛楃"""
        escape_map = {
            'n': '\n',
            't': '\t',
            '\\': '\\',
            '"': '"',
            "'": "'",
        }
        return escape_map.get(char, char)
    
    def _parse_number(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽鏁板瓧瀛楅潰閲?""
        position = start
        
        # 瑙ｆ瀽鏁存暟閮ㄥ垎
        while position < len(line) and line[position].isdigit():
            position += 1
        
        # 瑙ｆ瀽灏忔暟閮ㄥ垎
        if position < len(line) and line[position] == '.':
            position += 1
            while position < len(line) and line[position].isdigit():
                position += 1
        
        # 瑙ｆ瀽绉戝璁℃暟娉?        if position < len(line) and line[position].lower() == 'e':
            position += 1
            if position < len(line) and line[position] in ('+', '-'):
                position += 1
            while position < len(line) and line[position].isdigit():
                position += 1
        
        lexeme = line[start:position]
        
        # 灏濊瘯杞崲涓烘暟瀛?        try:
            if '.' in lexeme or 'e' in lexeme.lower():
                value = float(lexeme)
            else:
                value = int(lexeme)
        except ValueError:
            value = lexeme  # 淇濇寔鍘熸牱
        
        return Token(TokenType.NUMBER, value, line_num, column, lexeme)
    
    def _parse_chinese_number(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽涓枃鏁板瓧"""
        position = start
        lexeme = ''
        
        while position < len(line) and line[position] in self.chinese_numbers:
            lexeme += line[position]
            position += 1
        
        # 杞崲涓洪樋鎷変集鏁板瓧
        value = self._chinese_to_arabic(lexeme)
        
        return Token(TokenType.CHINESE_NUMBER, value, line_num, column, lexeme)
    
    def _chinese_to_arabic(self, chinese_num: str) -> int:
        """灏嗕腑鏂囨暟瀛楄浆鎹负闃挎媺浼暟瀛?""
        if not chinese_num:
            return 0
        
        # 绠€鍗曞疄鐜帮紝鍙鐞嗗熀鏈暟瀛?        total = 0
        current = 0
        
        for char in chinese_num:
            num = self.chinese_numbers.get(char, 0)
            
            if num < 10:
                current = num
            elif num >= 10:
                if current == 0:
                    current = 1
                total += current * num
                current = 0
        
        total += current
        return total
    
    def _parse_identifier(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽鏍囪瘑绗?""
        position = start
        
        # 鏀堕泦鏍囪瘑绗﹀瓧绗?        while position < len(line) and self._is_identifier_char(line[position]):
            position += 1
        
        lexeme = line[start:position]
        
        # 妫€鏌ユ槸鍚︿负鍏抽敭璇?        token_type = self._get_keyword_type(lexeme)
        if token_type:
            return Token(token_type, lexeme, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负鐧惧濮撳彉閲?        if self._is_bai_jia_xing(lexeme):
            return Token(TokenType.BAIJIAXING, lexeme, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负鍔ㄨ瘝
        arity = get_verb_arity(lexeme)
        if arity != 0:
            # 鏍规嵁鍏冩暟纭畾鍔ㄨ瘝绫诲瀷
            if arity == -1:
                token_type = TokenType.VERB_VAR
            elif arity == 0:
                token_type = TokenType.VERB_0
            elif arity == 1:
                token_type = TokenType.VERB_1
            elif arity == 2:
                token_type = TokenType.VERB_2
            elif arity == 3:
                token_type = TokenType.VERB_3
            else:
                token_type = TokenType.VERB_VAR
            
            return Token(token_type, lexeme, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负甯冨皵瀛楅潰閲?        if lexeme in ('鐪?, '鍋?, 'true', 'false', 'True', 'False'):
            value = lexeme in ('鐪?, 'true', 'True')
            return Token(TokenType.BOOLEAN, value, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负绌哄€?        if lexeme == '绌?:
            return Token(TokenType.NULL, None, line_num, column, lexeme)
        
        # 灏濊瘯涓枃鍒嗚瘝
        if len(lexeme) > 1 and any('\u4e00' <= c <= '\u9fff' for c in lexeme):
            # 浣跨敤jieba杩涜涓枃鍒嗚瘝
            segments = self._segment(lexeme)
            if len(segments) > 1:
                # 濡傛灉鏄涓瘝锛岃繑鍥炵涓€涓瘝浣滀负鏍囪瘑绗?                first_segment = segments[0]
                # 閫掑綊澶勭悊绗竴涓瘝
                return self._parse_identifier(first_segment, 0, line_num, column)
        
        # 鏅€氭爣璇嗙
        return Token(TokenType.IDENTIFIER, lexeme, line_num, column, lexeme)
    
    def _is_identifier_char(self, char: str) -> bool:
        """妫€鏌ュ瓧绗︽槸鍚︿负鏍囪瘑绗﹀瓧绗?""
        # 涓枃瀛楃銆佽嫳鏂囧瓧姣嶃€佹暟瀛椼€佷笅鍒掔嚎
        return ('\u4e00' <= char <= '\u9fff' or
                'a' <= char <= 'z' or
                'A' <= char <= 'Z' or
                char.isdigit() or
                char == '_')
    
    def _get_keyword_type(self, lexeme: str) -> Optional[TokenType]:
        """鑾峰彇鍏抽敭璇嶇被鍨?""
        # 妫€鏌ョ姸鎬佸叧閿瘝锛堝瀛楋級
        for keyword, token_type in self.state_keywords.items():
            if lexeme.startswith(keyword):
                return token_type
        
        # 妫€鏌ユ劅鐭ュ叧閿瘝锛堝瀛楋級
        for keyword, token_type in self.perception_keywords.items():
            if lexeme.startswith(keyword):
                return token_type
        
        # 妫€鏌ユ椂闂村叧閿瘝锛堝瀛楋級
        for keyword, token_type in self.time_keywords.items():
            if lexeme.startswith(keyword):
                return token_type
        
        # 妫€鏌ユ櫘閫氬叧閿瘝
        return self.keywords.get(lexeme)
    
    def _is_bai_jia_xing(self, lexeme: str) -> bool:
        """妫€鏌ユ槸鍚︿负鐧惧濮撳彉閲?""
        if not lexeme:
            return False
        
        # 鑾峰彇濮撴皬锛堢涓€涓瓧绗︼級
        surname = lexeme[0]
        
        # 妫€鏌ユ槸鍚︿负鍐茬獊濮撴皬
        if surname in self.conflict_surnames:
            return False
        
        # 妫€鏌ユ槸鍚︿负鐧惧濮?        return surname in self.bai_jia_xing
    
    def print_tokens(self, tokens: List[Token]) -> None:
        """鎵撳嵃璇嶆硶鍗曞厓鍒楄〃"""
        print("璇嶆硶鍒嗘瀽缁撴灉:")
        print("=" * 80)
        print(f"{'琛?:<4} {'鍒?:<4} {'绫诲瀷':<20} {'鍊?:<20} {'璇嶇礌':<20}")
        print("-" * 80)
        
        for token in tokens:
            value_str = str(token.value)
            if len(value_str) > 18:
                value_str = value_str[:15] + "..."
            
            lexeme_str = token.lexeme
            if len(lexeme_str) > 18:
                lexeme_str = lexeme_str[:15] + "..."
            
            print(f"{token.line:<4} {token.column:<4} {token.type.value:<20} {value_str:<20} {lexeme_str:<20}")
        
        print("=" * 80)


# 娴嬭瘯鍑芥暟
def test_lexer():
    """娴嬭瘯璇嶆硶鍒嗘瀽鍣?""
    print("璇嶆硶鍒嗘瀽鍣ㄦ祴璇?)
    print("=" * 50)
    
    lexer = YanLuLexer()
    
    # 娴嬭瘯鐢ㄤ緥
    test_cases = [
        (
            "瀹氭俯搴︽槸25銆?,
            "鍙橀噺瀹氫箟"
        ),
        (
            "濡傛灉娓╁害澶?0灏卞紑鍚鎵囥€?,
            "鏉′欢璇彞"
        ),
        (
            "瀵逛簬i鍦?鍒?0锛氬嵃i銆?,
            "寰幆璇彞"
        ),
        (
            "娓╁害鍙樹负30搴︺€?,
            "鐘舵€佽浆鎹?
        ),
        (
            "寮犱笁銆佹潕鍥涳紝璁＄畻鎶樻墸銆?,
            "鎰忓悎寮忓嚱鏁拌皟鐢?
        ),
        (
            "'浣犲ソ锛屼笘鐣?",
            "瀛楃涓插瓧闈㈤噺"
        ),
        (
            "鐪熶笖鍋?,
            "甯冨皵杩愮畻"
        ),
        (
            "瀹歺绛変簬鍗佸姞浜斻€?,
            "涓枃鏁板瓧"
        ),
    ]
    
    for source_code, description in test_cases:
        print(f"\n娴嬭瘯: {description}")
        print(f"婧愪唬鐮? {source_code}")
        
        try:
            tokens = lexer.tokenize(source_code)
            lexer.print_tokens(tokens)
        except Exception as e:
            print(f"閿欒: {e}")
    
    print("=" * 50)
    print("娴嬭瘯瀹屾垚")


if __name__ == "__main__":
    test_lexer())
        self.identifier_pattern = re.compile(r'^[\u4e00-\u9fffA-Za-z_][\u4e00-\u9fffA-Za-z0-9_]*
        """
        灏嗘簮浠ｇ爜杞崲涓鸿瘝娉曞崟鍏冨垪琛?        
        Args:
            source_code: 婧愪唬鐮佸瓧绗︿覆
            
        Returns:
            璇嶆硶鍗曞厓鍒楄〃
        """
        tokens = []
        lines = source_code.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            line_tokens = self._tokenize_line(line, line_num)
            tokens.extend(line_tokens)
            
            # 娣诲姞鎹㈣绗︼紙闄ら潪鏄渶鍚庝竴琛岋級
            if line_num < len(lines):
                tokens.append(Token(TokenType.NEWLINE, '\n', line_num, len(line) + 1, '\n'))
        
        # 娣诲姞鏂囦欢缁撴潫鏍囪
        tokens.append(Token(TokenType.EOF, '', len(lines) + 1, 1, ''))
        
        return tokens
    
    def _tokenize_line(self, line: str, line_num: int) -> List[Token]:
        """灏嗕竴琛屼唬鐮佽浆鎹负璇嶆硶鍗曞厓鍒楄〃"""
        tokens = []
        position = 0
        column = 1
        
        # 浣跨敤鍒嗚瘝鍣ㄨ繘琛屼腑鏂囧垎璇?        segments = self._segment(line)
        segment_index = 0
        
        while position < len(line):
            # 璺宠繃绌虹櫧瀛楃
            if line[position].isspace():
                if line[position] == '\n':
                    tokens.append(Token(TokenType.NEWLINE, '\n', line_num, column, '\n'))
                position += 1
                column += 1
                continue
            
            # 澶勭悊娉ㄩ噴
            if line[position] == '#':
                # 鍗曡娉ㄩ噴锛岃烦杩囨暣琛?                comment = line[position:]
                tokens.append(Token(TokenType.COMMENT, comment, line_num, column, comment))
                break
            
            # 澶勭悊澶氳瑷€浠ｇ爜鍧?            if line[position:position+2] == '{{':
                tokens.append(Token(TokenType.CODE_BLOCK_START, '{{', line_num, column, '{{'))
                position += 2
                column += 2
                continue
            
            if line[position:position+2] == '}}':
                tokens.append(Token(TokenType.CODE_BLOCK_END, '}}', line_num, column, '}}'))
                position += 2
                column += 2
                continue
            
            # 澶勭悊涓枃鏍囩偣绗﹀彿
            if line[position] in self.chinese_punctuation:
                char = line[position]
                token_type = self.chinese_punctuation[char]
                
                # 澶勭悊鎴愬鏍囩偣绗﹀彿
                if char in ('銆?, '銆?):
                    # 鏌ユ壘鍖归厤鐨勭粨鏉熺鍙?                    end_pos = line.find('銆? if char == '銆? else '銆?, position + 1)
                    if end_pos != -1:
                        value = line[position:end_pos + 1]
                        tokens.append(Token(token_type, value, line_num, column, value))
                        position = end_pos + 1
                        column += len(value)
                        continue
                
                tokens.append(Token(token_type, char, line_num, column, char))
                position += 1
                column += 1
                continue
            
            # 澶勭悊鐪佺暐鍙?            if line[position:position+2] == '鈥︹€?:
                tokens.append(Token(TokenType.ELLIPSIS, '鈥︹€?, line_num, column, '鈥︹€?))
                position += 2
                column += 2
                continue
            
            # 澶勭悊鐮存姌鍙?            if line[position:position+2] == '鈥斺€?:
                tokens.append(Token(TokenType.DASH, '鈥斺€?, line_num, column, '鈥斺€?))
                position += 2
                column += 2
                continue
            
            # 澶勭悊鍦嗗湀鍙?            if line[position] in '鈶犫憽鈶⑩懀鈶も懃鈶︹懅鈶ㄢ懇':
                tokens.append(Token(TokenType.CIRCLED_NUMBERS, line[position], line_num, column, line[position]))
                position += 1
                column += 1
                continue
            
            # 澶勭悊杩愮畻绗?            if line[position] in self.operators:
                # 妫€鏌ュ弻瀛楃杩愮畻绗?                if position + 1 < len(line):
                    two_char = line[position:position+2]
                    if two_char in ('鈮?, '鈮?, '鈮?):
                        tokens.append(Token(self.operators[two_char], two_char, line_num, column, two_char))
                        position += 2
                        column += 2
                        continue
                
                tokens.append(Token(self.operators[line[position]], line[position], line_num, column, line[position]))
                position += 1
                column += 1
                continue
            
            # 澶勭悊鍒嗙粍绗﹀彿
            if line[position] in self.grouping_symbols:
                tokens.append(Token(self.grouping_symbols[line[position]], line[position], line_num, column, line[position]))
                position += 1
                column += 1
                continue
            
            # 澶勭悊瀛楃涓插瓧闈㈤噺
            if line[position] in ('"', "'"):
                string_token = self._parse_string_literal(line, position, line_num, column)
                tokens.append(string_token)
                position += len(string_token.lexeme)
                column += len(string_token.lexeme)
                continue
            
            # 澶勭悊鏁板瓧瀛楅潰閲?            if line[position].isdigit() or (line[position] == '.' and position + 1 < len(line) and line[position + 1].isdigit()):
                number_token = self._parse_number(line, position, line_num, column)
                tokens.append(number_token)
                position += len(number_token.lexeme)
                column += len(number_token.lexeme)
                continue
            
            # 澶勭悊涓枃鏁板瓧
            if line[position] in self.chinese_numbers:
                chinese_number_token = self._parse_chinese_number(line, position, line_num, column)
                tokens.append(chinese_number_token)
                position += len(chinese_number_token.lexeme)
                column += len(chinese_number_token.lexeme)
                continue
            
            # 澶勭悊褰撳墠鍒嗚瘝娈?            if segment_index < len(segments):
                segment = segments[segment_index].strip()
                if segment:  # 璺宠繃绌哄垎璇?                    # 澶勭悊鍒嗚瘝娈?                    token = self._process_segment(segment, line_num, column)
                    tokens.append(token)
                    position += len(segment)
                    column += len(segment)
                segment_index += 1
            else:
                # 濡傛灉娌℃湁鏇村鍒嗚瘝锛屽鐞嗗墿浣欏瓧绗?                identifier_token = self._parse_identifier(line, position, line_num, column)
                tokens.append(identifier_token)
                position += len(identifier_token.lexeme)
                column += len(identifier_token.lexeme)
        
        return tokens
    
    def _process_segment(self, segment: str, line_num: int, column: int) -> Token:
        """澶勭悊鍒嗚瘝娈?""
        # 妫€鏌ユ槸鍚︿负鍏抽敭璇?        token_type = self._get_keyword_type(segment)
        if token_type:
            return Token(token_type, segment, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负鐧惧濮撳彉閲?        if self._is_bai_jia_xing(segment):
            return Token(TokenType.BAIJIAXING, segment, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负鍔ㄨ瘝
        arity = get_verb_arity(segment)
        if arity != 0:
            # 鏍规嵁鍏冩暟纭畾鍔ㄨ瘝绫诲瀷
            if arity == -1:
                token_type = TokenType.VERB_VAR
            elif arity == 0:
                token_type = TokenType.VERB_0
            elif arity == 1:
                token_type = TokenType.VERB_1
            elif arity == 2:
                token_type = TokenType.VERB_2
            elif arity == 3:
                token_type = TokenType.VERB_3
            else:
                token_type = TokenType.VERB_VAR
            
            return Token(token_type, segment, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负甯冨皵瀛楅潰閲?        if segment in ('鐪?, '鍋?, 'true', 'false', 'True', 'False'):
            value = segment in ('鐪?, 'true', 'True')
            return Token(TokenType.BOOLEAN, value, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负绌哄€?        if segment == '绌?:
            return Token(TokenType.NULL, None, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负鏁板瓧
        if segment.isdigit() or (segment.replace('.', '', 1).isdigit() and segment.count('.') == 1):
            try:
                if '.' in segment:
                    value = float(segment)
                else:
                    value = int(segment)
                return Token(TokenType.NUMBER, value, line_num, column, segment)
            except ValueError:
                pass
        
        # 妫€鏌ユ槸鍚︿负涓枃鏁板瓧
        if all(c in self.chinese_numbers for c in segment):
            value = self._chinese_to_arabic(segment)
            return Token(TokenType.CHINESE_NUMBER, value, line_num, column, segment)
        
        # 鏅€氭爣璇嗙
        return Token(TokenType.IDENTIFIER, segment, line_num, column, segment)
    
    def _parse_string_literal(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽瀛楃涓插瓧闈㈤噺"""
        quote_char = line[start]
        position = start + 1
        value = ''
        
        while position < len(line):
            char = line[position]
            
            if char == quote_char:
                # 缁撴潫寮曞彿
                position += 1
                break
            elif char == '\\' and position + 1 < len(line):
                # 杞箟瀛楃
                next_char = line[position + 1]
                if next_char in ('n', 't', '\\', '"', "'"):
                    value += self._escape_char(next_char)
                    position += 2
                else:
                    value += char
                    position += 1
            else:
                value += char
                position += 1
        
        lexeme = line[start:position]
        return Token(TokenType.STRING, value, line_num, column, lexeme)
    
    def _escape_char(self, char: str) -> str:
        """杞箟瀛楃"""
        escape_map = {
            'n': '\n',
            't': '\t',
            '\\': '\\',
            '"': '"',
            "'": "'",
        }
        return escape_map.get(char, char)
    
    def _parse_number(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽鏁板瓧瀛楅潰閲?""
        position = start
        
        # 瑙ｆ瀽鏁存暟閮ㄥ垎
        while position < len(line) and line[position].isdigit():
            position += 1
        
        # 瑙ｆ瀽灏忔暟閮ㄥ垎
        if position < len(line) and line[position] == '.':
            position += 1
            while position < len(line) and line[position].isdigit():
                position += 1
        
        # 瑙ｆ瀽绉戝璁℃暟娉?        if position < len(line) and line[position].lower() == 'e':
            position += 1
            if position < len(line) and line[position] in ('+', '-'):
                position += 1
            while position < len(line) and line[position].isdigit():
                position += 1
        
        lexeme = line[start:position]
        
        # 灏濊瘯杞崲涓烘暟瀛?        try:
            if '.' in lexeme or 'e' in lexeme.lower():
                value = float(lexeme)
            else:
                value = int(lexeme)
        except ValueError:
            value = lexeme  # 淇濇寔鍘熸牱
        
        return Token(TokenType.NUMBER, value, line_num, column, lexeme)
    
    def _parse_chinese_number(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽涓枃鏁板瓧"""
        position = start
        lexeme = ''
        
        while position < len(line) and line[position] in self.chinese_numbers:
            lexeme += line[position]
            position += 1
        
        # 杞崲涓洪樋鎷変集鏁板瓧
        value = self._chinese_to_arabic(lexeme)
        
        return Token(TokenType.CHINESE_NUMBER, value, line_num, column, lexeme)
    
    def _chinese_to_arabic(self, chinese_num: str) -> int:
        """灏嗕腑鏂囨暟瀛楄浆鎹负闃挎媺浼暟瀛?""
        if not chinese_num:
            return 0
        
        # 绠€鍗曞疄鐜帮紝鍙鐞嗗熀鏈暟瀛?        total = 0
        current = 0
        
        for char in chinese_num:
            num = self.chinese_numbers.get(char, 0)
            
            if num < 10:
                current = num
            elif num >= 10:
                if current == 0:
                    current = 1
                total += current * num
                current = 0
        
        total += current
        return total
    
    def _parse_identifier(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽鏍囪瘑绗?""
        position = start
        
        # 鏀堕泦鏍囪瘑绗﹀瓧绗?        while position < len(line) and self._is_identifier_char(line[position]):
            position += 1
        
        lexeme = line[start:position]
        
        # 妫€鏌ユ槸鍚︿负鍏抽敭璇?        token_type = self._get_keyword_type(lexeme)
        if token_type:
            return Token(token_type, lexeme, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负鐧惧濮撳彉閲?        if self._is_bai_jia_xing(lexeme):
            return Token(TokenType.BAIJIAXING, lexeme, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负鍔ㄨ瘝
        arity = get_verb_arity(lexeme)
        if arity != 0:
            # 鏍规嵁鍏冩暟纭畾鍔ㄨ瘝绫诲瀷
            if arity == -1:
                token_type = TokenType.VERB_VAR
            elif arity == 0:
                token_type = TokenType.VERB_0
            elif arity == 1:
                token_type = TokenType.VERB_1
            elif arity == 2:
                token_type = TokenType.VERB_2
            elif arity == 3:
                token_type = TokenType.VERB_3
            else:
                token_type = TokenType.VERB_VAR
            
            return Token(token_type, lexeme, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负甯冨皵瀛楅潰閲?        if lexeme in ('鐪?, '鍋?, 'true', 'false', 'True', 'False'):
            value = lexeme in ('鐪?, 'true', 'True')
            return Token(TokenType.BOOLEAN, value, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负绌哄€?        if lexeme == '绌?:
            return Token(TokenType.NULL, None, line_num, column, lexeme)
        
        # 灏濊瘯涓枃鍒嗚瘝
        if len(lexeme) > 1 and any('\u4e00' <= c <= '\u9fff' for c in lexeme):
            # 浣跨敤jieba杩涜涓枃鍒嗚瘝
            segments = self._segment(lexeme)
            if len(segments) > 1:
                # 濡傛灉鏄涓瘝锛岃繑鍥炵涓€涓瘝浣滀负鏍囪瘑绗?                first_segment = segments[0]
                # 閫掑綊澶勭悊绗竴涓瘝
                return self._parse_identifier(first_segment, 0, line_num, column)
        
        # 鏅€氭爣璇嗙
        return Token(TokenType.IDENTIFIER, lexeme, line_num, column, lexeme)
    
    def _is_identifier_char(self, char: str) -> bool:
        """妫€鏌ュ瓧绗︽槸鍚︿负鏍囪瘑绗﹀瓧绗?""
        # 涓枃瀛楃銆佽嫳鏂囧瓧姣嶃€佹暟瀛椼€佷笅鍒掔嚎
        return ('\u4e00' <= char <= '\u9fff' or
                'a' <= char <= 'z' or
                'A' <= char <= 'Z' or
                char.isdigit() or
                char == '_')
    
    def _get_keyword_type(self, lexeme: str) -> Optional[TokenType]:
        """鑾峰彇鍏抽敭璇嶇被鍨?""
        # 妫€鏌ョ姸鎬佸叧閿瘝锛堝瀛楋級
        for keyword, token_type in self.state_keywords.items():
            if lexeme.startswith(keyword):
                return token_type
        
        # 妫€鏌ユ劅鐭ュ叧閿瘝锛堝瀛楋級
        for keyword, token_type in self.perception_keywords.items():
            if lexeme.startswith(keyword):
                return token_type
        
        # 妫€鏌ユ椂闂村叧閿瘝锛堝瀛楋級
        for keyword, token_type in self.time_keywords.items():
            if lexeme.startswith(keyword):
                return token_type
        
        # 妫€鏌ユ櫘閫氬叧閿瘝
        return self.keywords.get(lexeme)
    
    def _is_bai_jia_xing(self, lexeme: str) -> bool:
        """妫€鏌ユ槸鍚︿负鐧惧濮撳彉閲?""
        if not lexeme:
            return False
        
        # 鑾峰彇濮撴皬锛堢涓€涓瓧绗︼級
        surname = lexeme[0]
        
        # 妫€鏌ユ槸鍚︿负鍐茬獊濮撴皬
        if surname in self.conflict_surnames:
            return False
        
        # 妫€鏌ユ槸鍚︿负鐧惧濮?        return surname in self.bai_jia_xing
    
    def print_tokens(self, tokens: List[Token]) -> None:
        """鎵撳嵃璇嶆硶鍗曞厓鍒楄〃"""
        print("璇嶆硶鍒嗘瀽缁撴灉:")
        print("=" * 80)
        print(f"{'琛?:<4} {'鍒?:<4} {'绫诲瀷':<20} {'鍊?:<20} {'璇嶇礌':<20}")
        print("-" * 80)
        
        for token in tokens:
            value_str = str(token.value)
            if len(value_str) > 18:
                value_str = value_str[:15] + "..."
            
            lexeme_str = token.lexeme
            if len(lexeme_str) > 18:
                lexeme_str = lexeme_str[:15] + "..."
            
            print(f"{token.line:<4} {token.column:<4} {token.type.value:<20} {value_str:<20} {lexeme_str:<20}")
        
        print("=" * 80)


# 娴嬭瘯鍑芥暟
def test_lexer():
    """娴嬭瘯璇嶆硶鍒嗘瀽鍣?""
    print("璇嶆硶鍒嗘瀽鍣ㄦ祴璇?)
    print("=" * 50)
    
    lexer = YanLuLexer()
    
    # 娴嬭瘯鐢ㄤ緥
    test_cases = [
        (
            "瀹氭俯搴︽槸25銆?,
            "鍙橀噺瀹氫箟"
        ),
        (
            "濡傛灉娓╁害澶?0灏卞紑鍚鎵囥€?,
            "鏉′欢璇彞"
        ),
        (
            "瀵逛簬i鍦?鍒?0锛氬嵃i銆?,
            "寰幆璇彞"
        ),
        (
            "娓╁害鍙樹负30搴︺€?,
            "鐘舵€佽浆鎹?
        ),
        (
            "寮犱笁銆佹潕鍥涳紝璁＄畻鎶樻墸銆?,
            "鎰忓悎寮忓嚱鏁拌皟鐢?
        ),
        (
            "'浣犲ソ锛屼笘鐣?",
            "瀛楃涓插瓧闈㈤噺"
        ),
        (
            "鐪熶笖鍋?,
            "甯冨皵杩愮畻"
        ),
        (
            "瀹歺绛変簬鍗佸姞浜斻€?,
            "涓枃鏁板瓧"
        ),
    ]
    
    for source_code, description in test_cases:
        print(f"\n娴嬭瘯: {description}")
        print(f"婧愪唬鐮? {source_code}")
        
        try:
            tokens = lexer.tokenize(source_code)
            lexer.print_tokens(tokens)
        except Exception as e:
            print(f"閿欒: {e}")
    
    print("=" * 50)
    print("娴嬭瘯瀹屾垚")


if __name__ == "__main__":
    test_lexer())
    
    def _init_segmenter(self):
        """鍒濆鍖栧垎璇嶅櫒"""
        if self.segmenter_type == "thulac":
            try:
                import thulac
                # 浣跨敤seg_only=True鍙繘琛屽垎璇嶏紝涓嶈繘琛岃瘝鎬ф爣娉?                self.segmenter = thulac.thulac(seg_only=True, model_path=None)
                print(f"浣跨敤THULAC鍒嗚瘝鍣?(seg_only妯″紡)")
            except ImportError:
                print("璀﹀憡: 鏈畨瑁匱HULAC锛屽洖閫€鍒癹ieba鍒嗚瘝鍣?)
                print("瀹夎鍛戒护: pip install thulac")
                self.segmenter_type = "jieba"
                self.segmenter = jieba
        else:
            # 榛樿浣跨敤jieba
            self.segmenter = jieba
            print(f"浣跨敤jieba鍒嗚瘝鍣?)
    
    def _segment(self, text: str) -> List[str]:
        """
        鍒嗚瘝鏂规硶
        
        Args:
            text: 寰呭垎璇嶇殑鏂囨湰
            
        Returns:
            鍒嗚瘝缁撴灉鍒楄〃
        """
        if self.segmenter_type == "thulac":
            # THULAC鍒嗚瘝
            result = self.segmenter.cut(text, text=True)
            return result.split()
        else:
            # jieba鍒嗚瘝
            return list(self.segmenter.lcut(text))
        
    def tokenize(self, source_code: str) -> List[Token]:
        """
        灏嗘簮浠ｇ爜杞崲涓鸿瘝娉曞崟鍏冨垪琛?        
        Args:
            source_code: 婧愪唬鐮佸瓧绗︿覆
            
        Returns:
            璇嶆硶鍗曞厓鍒楄〃
        """
        tokens = []
        lines = source_code.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            line_tokens = self._tokenize_line(line, line_num)
            tokens.extend(line_tokens)
            
            # 娣诲姞鎹㈣绗︼紙闄ら潪鏄渶鍚庝竴琛岋級
            if line_num < len(lines):
                tokens.append(Token(TokenType.NEWLINE, '\n', line_num, len(line) + 1, '\n'))
        
        # 娣诲姞鏂囦欢缁撴潫鏍囪
        tokens.append(Token(TokenType.EOF, '', len(lines) + 1, 1, ''))
        
        return tokens
    
    def _tokenize_line(self, line: str, line_num: int) -> List[Token]:
        """灏嗕竴琛屼唬鐮佽浆鎹负璇嶆硶鍗曞厓鍒楄〃"""
        tokens = []
        position = 0
        column = 1
        
        # 浣跨敤鍒嗚瘝鍣ㄨ繘琛屼腑鏂囧垎璇?        segments = self._segment(line)
        segment_index = 0
        
        while position < len(line):
            # 璺宠繃绌虹櫧瀛楃
            if line[position].isspace():
                if line[position] == '\n':
                    tokens.append(Token(TokenType.NEWLINE, '\n', line_num, column, '\n'))
                position += 1
                column += 1
                continue
            
            # 澶勭悊娉ㄩ噴
            if line[position] == '#':
                # 鍗曡娉ㄩ噴锛岃烦杩囨暣琛?                comment = line[position:]
                tokens.append(Token(TokenType.COMMENT, comment, line_num, column, comment))
                break
            
            # 澶勭悊澶氳瑷€浠ｇ爜鍧?            if line[position:position+2] == '{{':
                tokens.append(Token(TokenType.CODE_BLOCK_START, '{{', line_num, column, '{{'))
                position += 2
                column += 2
                continue
            
            if line[position:position+2] == '}}':
                tokens.append(Token(TokenType.CODE_BLOCK_END, '}}', line_num, column, '}}'))
                position += 2
                column += 2
                continue
            
            # 澶勭悊涓枃鏍囩偣绗﹀彿
            if line[position] in self.chinese_punctuation:
                char = line[position]
                token_type = self.chinese_punctuation[char]
                
                # 澶勭悊鎴愬鏍囩偣绗﹀彿
                if char in ('銆?, '銆?):
                    # 鏌ユ壘鍖归厤鐨勭粨鏉熺鍙?                    end_pos = line.find('銆? if char == '銆? else '銆?, position + 1)
                    if end_pos != -1:
                        value = line[position:end_pos + 1]
                        tokens.append(Token(token_type, value, line_num, column, value))
                        position = end_pos + 1
                        column += len(value)
                        continue
                
                tokens.append(Token(token_type, char, line_num, column, char))
                position += 1
                column += 1
                continue
            
            # 澶勭悊鐪佺暐鍙?            if line[position:position+2] == '鈥︹€?:
                tokens.append(Token(TokenType.ELLIPSIS, '鈥︹€?, line_num, column, '鈥︹€?))
                position += 2
                column += 2
                continue
            
            # 澶勭悊鐮存姌鍙?            if line[position:position+2] == '鈥斺€?:
                tokens.append(Token(TokenType.DASH, '鈥斺€?, line_num, column, '鈥斺€?))
                position += 2
                column += 2
                continue
            
            # 澶勭悊鍦嗗湀鍙?            if line[position] in '鈶犫憽鈶⑩懀鈶も懃鈶︹懅鈶ㄢ懇':
                tokens.append(Token(TokenType.CIRCLED_NUMBERS, line[position], line_num, column, line[position]))
                position += 1
                column += 1
                continue
            
            # 澶勭悊杩愮畻绗?            if line[position] in self.operators:
                # 妫€鏌ュ弻瀛楃杩愮畻绗?                if position + 1 < len(line):
                    two_char = line[position:position+2]
                    if two_char in ('鈮?, '鈮?, '鈮?):
                        tokens.append(Token(self.operators[two_char], two_char, line_num, column, two_char))
                        position += 2
                        column += 2
                        continue
                
                tokens.append(Token(self.operators[line[position]], line[position], line_num, column, line[position]))
                position += 1
                column += 1
                continue
            
            # 澶勭悊鍒嗙粍绗﹀彿
            if line[position] in self.grouping_symbols:
                tokens.append(Token(self.grouping_symbols[line[position]], line[position], line_num, column, line[position]))
                position += 1
                column += 1
                continue
            
            # 澶勭悊瀛楃涓插瓧闈㈤噺
            if line[position] in ('"', "'"):
                string_token = self._parse_string_literal(line, position, line_num, column)
                tokens.append(string_token)
                position += len(string_token.lexeme)
                column += len(string_token.lexeme)
                continue
            
            # 澶勭悊鏁板瓧瀛楅潰閲?            if line[position].isdigit() or (line[position] == '.' and position + 1 < len(line) and line[position + 1].isdigit()):
                number_token = self._parse_number(line, position, line_num, column)
                tokens.append(number_token)
                position += len(number_token.lexeme)
                column += len(number_token.lexeme)
                continue
            
            # 澶勭悊涓枃鏁板瓧
            if line[position] in self.chinese_numbers:
                chinese_number_token = self._parse_chinese_number(line, position, line_num, column)
                tokens.append(chinese_number_token)
                position += len(chinese_number_token.lexeme)
                column += len(chinese_number_token.lexeme)
                continue
            
            # 澶勭悊褰撳墠鍒嗚瘝娈?            if segment_index < len(segments):
                segment = segments[segment_index].strip()
                if segment:  # 璺宠繃绌哄垎璇?                    # 澶勭悊鍒嗚瘝娈?                    token = self._process_segment(segment, line_num, column)
                    tokens.append(token)
                    position += len(segment)
                    column += len(segment)
                segment_index += 1
            else:
                # 濡傛灉娌℃湁鏇村鍒嗚瘝锛屽鐞嗗墿浣欏瓧绗?                identifier_token = self._parse_identifier(line, position, line_num, column)
                tokens.append(identifier_token)
                position += len(identifier_token.lexeme)
                column += len(identifier_token.lexeme)
        
        return tokens
    
    def _process_segment(self, segment: str, line_num: int, column: int) -> Token:
        """澶勭悊鍒嗚瘝娈?""
        # 妫€鏌ユ槸鍚︿负鍏抽敭璇?        token_type = self._get_keyword_type(segment)
        if token_type:
            return Token(token_type, segment, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负鐧惧濮撳彉閲?        if self._is_bai_jia_xing(segment):
            return Token(TokenType.BAIJIAXING, segment, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负鍔ㄨ瘝
        arity = get_verb_arity(segment)
        if arity != 0:
            # 鏍规嵁鍏冩暟纭畾鍔ㄨ瘝绫诲瀷
            if arity == -1:
                token_type = TokenType.VERB_VAR
            elif arity == 0:
                token_type = TokenType.VERB_0
            elif arity == 1:
                token_type = TokenType.VERB_1
            elif arity == 2:
                token_type = TokenType.VERB_2
            elif arity == 3:
                token_type = TokenType.VERB_3
            else:
                token_type = TokenType.VERB_VAR
            
            return Token(token_type, segment, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负甯冨皵瀛楅潰閲?        if segment in ('鐪?, '鍋?, 'true', 'false', 'True', 'False'):
            value = segment in ('鐪?, 'true', 'True')
            return Token(TokenType.BOOLEAN, value, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负绌哄€?        if segment == '绌?:
            return Token(TokenType.NULL, None, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负鏁板瓧
        if segment.isdigit() or (segment.replace('.', '', 1).isdigit() and segment.count('.') == 1):
            try:
                if '.' in segment:
                    value = float(segment)
                else:
                    value = int(segment)
                return Token(TokenType.NUMBER, value, line_num, column, segment)
            except ValueError:
                pass
        
        # 妫€鏌ユ槸鍚︿负涓枃鏁板瓧
        if all(c in self.chinese_numbers for c in segment):
            value = self._chinese_to_arabic(segment)
            return Token(TokenType.CHINESE_NUMBER, value, line_num, column, segment)
        
        # 鏅€氭爣璇嗙
        return Token(TokenType.IDENTIFIER, segment, line_num, column, segment)
    
    def _parse_string_literal(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽瀛楃涓插瓧闈㈤噺"""
        quote_char = line[start]
        position = start + 1
        value = ''
        
        while position < len(line):
            char = line[position]
            
            if char == quote_char:
                # 缁撴潫寮曞彿
                position += 1
                break
            elif char == '\\' and position + 1 < len(line):
                # 杞箟瀛楃
                next_char = line[position + 1]
                if next_char in ('n', 't', '\\', '"', "'"):
                    value += self._escape_char(next_char)
                    position += 2
                else:
                    value += char
                    position += 1
            else:
                value += char
                position += 1
        
        lexeme = line[start:position]
        return Token(TokenType.STRING, value, line_num, column, lexeme)
    
    def _escape_char(self, char: str) -> str:
        """杞箟瀛楃"""
        escape_map = {
            'n': '\n',
            't': '\t',
            '\\': '\\',
            '"': '"',
            "'": "'",
        }
        return escape_map.get(char, char)
    
    def _parse_number(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽鏁板瓧瀛楅潰閲?""
        position = start
        
        # 瑙ｆ瀽鏁存暟閮ㄥ垎
        while position < len(line) and line[position].isdigit():
            position += 1
        
        # 瑙ｆ瀽灏忔暟閮ㄥ垎
        if position < len(line) and line[position] == '.':
            position += 1
            while position < len(line) and line[position].isdigit():
                position += 1
        
        # 瑙ｆ瀽绉戝璁℃暟娉?        if position < len(line) and line[position].lower() == 'e':
            position += 1
            if position < len(line) and line[position] in ('+', '-'):
                position += 1
            while position < len(line) and line[position].isdigit():
                position += 1
        
        lexeme = line[start:position]
        
        # 灏濊瘯杞崲涓烘暟瀛?        try:
            if '.' in lexeme or 'e' in lexeme.lower():
                value = float(lexeme)
            else:
                value = int(lexeme)
        except ValueError:
            value = lexeme  # 淇濇寔鍘熸牱
        
        return Token(TokenType.NUMBER, value, line_num, column, lexeme)
    
    def _parse_chinese_number(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽涓枃鏁板瓧"""
        position = start
        lexeme = ''
        
        while position < len(line) and line[position] in self.chinese_numbers:
            lexeme += line[position]
            position += 1
        
        # 杞崲涓洪樋鎷変集鏁板瓧
        value = self._chinese_to_arabic(lexeme)
        
        return Token(TokenType.CHINESE_NUMBER, value, line_num, column, lexeme)
    
    def _chinese_to_arabic(self, chinese_num: str) -> int:
        """灏嗕腑鏂囨暟瀛楄浆鎹负闃挎媺浼暟瀛?""
        if not chinese_num:
            return 0
        
        # 绠€鍗曞疄鐜帮紝鍙鐞嗗熀鏈暟瀛?        total = 0
        current = 0
        
        for char in chinese_num:
            num = self.chinese_numbers.get(char, 0)
            
            if num < 10:
                current = num
            elif num >= 10:
                if current == 0:
                    current = 1
                total += current * num
                current = 0
        
        total += current
        return total
    
    def _parse_identifier(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽鏍囪瘑绗?""
        position = start
        
        # 鏀堕泦鏍囪瘑绗﹀瓧绗?        while position < len(line) and self._is_identifier_char(line[position]):
            position += 1
        
        lexeme = line[start:position]
        
        # 妫€鏌ユ槸鍚︿负鍏抽敭璇?        token_type = self._get_keyword_type(lexeme)
        if token_type:
            return Token(token_type, lexeme, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负鐧惧濮撳彉閲?        if self._is_bai_jia_xing(lexeme):
            return Token(TokenType.BAIJIAXING, lexeme, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负鍔ㄨ瘝
        arity = get_verb_arity(lexeme)
        if arity != 0:
            # 鏍规嵁鍏冩暟纭畾鍔ㄨ瘝绫诲瀷
            if arity == -1:
                token_type = TokenType.VERB_VAR
            elif arity == 0:
                token_type = TokenType.VERB_0
            elif arity == 1:
                token_type = TokenType.VERB_1
            elif arity == 2:
                token_type = TokenType.VERB_2
            elif arity == 3:
                token_type = TokenType.VERB_3
            else:
                token_type = TokenType.VERB_VAR
            
            return Token(token_type, lexeme, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负甯冨皵瀛楅潰閲?        if lexeme in ('鐪?, '鍋?, 'true', 'false', 'True', 'False'):
            value = lexeme in ('鐪?, 'true', 'True')
            return Token(TokenType.BOOLEAN, value, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负绌哄€?        if lexeme == '绌?:
            return Token(TokenType.NULL, None, line_num, column, lexeme)
        
        # 灏濊瘯涓枃鍒嗚瘝
        if len(lexeme) > 1 and any('\u4e00' <= c <= '\u9fff' for c in lexeme):
            # 浣跨敤jieba杩涜涓枃鍒嗚瘝
            segments = self._segment(lexeme)
            if len(segments) > 1:
                # 濡傛灉鏄涓瘝锛岃繑鍥炵涓€涓瘝浣滀负鏍囪瘑绗?                first_segment = segments[0]
                # 閫掑綊澶勭悊绗竴涓瘝
                return self._parse_identifier(first_segment, 0, line_num, column)
        
        # 鏅€氭爣璇嗙
        return Token(TokenType.IDENTIFIER, lexeme, line_num, column, lexeme)
    
    def _is_identifier_char(self, char: str) -> bool:
        """妫€鏌ュ瓧绗︽槸鍚︿负鏍囪瘑绗﹀瓧绗?""
        # 涓枃瀛楃銆佽嫳鏂囧瓧姣嶃€佹暟瀛椼€佷笅鍒掔嚎
        return ('\u4e00' <= char <= '\u9fff' or
                'a' <= char <= 'z' or
                'A' <= char <= 'Z' or
                char.isdigit() or
                char == '_')
    
    def _get_keyword_type(self, lexeme: str) -> Optional[TokenType]:
        """鑾峰彇鍏抽敭璇嶇被鍨?""
        # 妫€鏌ョ姸鎬佸叧閿瘝锛堝瀛楋級
        for keyword, token_type in self.state_keywords.items():
            if lexeme.startswith(keyword):
                return token_type
        
        # 妫€鏌ユ劅鐭ュ叧閿瘝锛堝瀛楋級
        for keyword, token_type in self.perception_keywords.items():
            if lexeme.startswith(keyword):
                return token_type
        
        # 妫€鏌ユ椂闂村叧閿瘝锛堝瀛楋級
        for keyword, token_type in self.time_keywords.items():
            if lexeme.startswith(keyword):
                return token_type
        
        # 妫€鏌ユ櫘閫氬叧閿瘝
        return self.keywords.get(lexeme)
    
    def _is_bai_jia_xing(self, lexeme: str) -> bool:
        """妫€鏌ユ槸鍚︿负鐧惧濮撳彉閲?""
        if not lexeme:
            return False
        
        # 鑾峰彇濮撴皬锛堢涓€涓瓧绗︼級
        surname = lexeme[0]
        
        # 妫€鏌ユ槸鍚︿负鍐茬獊濮撴皬
        if surname in self.conflict_surnames:
            return False
        
        # 妫€鏌ユ槸鍚︿负鐧惧濮?        return surname in self.bai_jia_xing
    
    def print_tokens(self, tokens: List[Token]) -> None:
        """鎵撳嵃璇嶆硶鍗曞厓鍒楄〃"""
        print("璇嶆硶鍒嗘瀽缁撴灉:")
        print("=" * 80)
        print(f"{'琛?:<4} {'鍒?:<4} {'绫诲瀷':<20} {'鍊?:<20} {'璇嶇礌':<20}")
        print("-" * 80)
        
        for token in tokens:
            value_str = str(token.value)
            if len(value_str) > 18:
                value_str = value_str[:15] + "..."
            
            lexeme_str = token.lexeme
            if len(lexeme_str) > 18:
                lexeme_str = lexeme_str[:15] + "..."
            
            print(f"{token.line:<4} {token.column:<4} {token.type.value:<20} {value_str:<20} {lexeme_str:<20}")
        
        print("=" * 80)


# 娴嬭瘯鍑芥暟
def test_lexer():
    """娴嬭瘯璇嶆硶鍒嗘瀽鍣?""
    print("璇嶆硶鍒嗘瀽鍣ㄦ祴璇?)
    print("=" * 50)
    
    lexer = YanLuLexer()
    
    # 娴嬭瘯鐢ㄤ緥
    test_cases = [
        (
            "瀹氭俯搴︽槸25銆?,
            "鍙橀噺瀹氫箟"
        ),
        (
            "濡傛灉娓╁害澶?0灏卞紑鍚鎵囥€?,
            "鏉′欢璇彞"
        ),
        (
            "瀵逛簬i鍦?鍒?0锛氬嵃i銆?,
            "寰幆璇彞"
        ),
        (
            "娓╁害鍙樹负30搴︺€?,
            "鐘舵€佽浆鎹?
        ),
        (
            "寮犱笁銆佹潕鍥涳紝璁＄畻鎶樻墸銆?,
            "鎰忓悎寮忓嚱鏁拌皟鐢?
        ),
        (
            "'浣犲ソ锛屼笘鐣?",
            "瀛楃涓插瓧闈㈤噺"
        ),
        (
            "鐪熶笖鍋?,
            "甯冨皵杩愮畻"
        ),
        (
            "瀹歺绛変簬鍗佸姞浜斻€?,
            "涓枃鏁板瓧"
        ),
    ]
    
    for source_code, description in test_cases:
        print(f"\n娴嬭瘯: {description}")
        print(f"婧愪唬鐮? {source_code}")
        
        try:
            tokens = lexer.tokenize(source_code)
            lexer.print_tokens(tokens)
        except Exception as e:
            print(f"閿欒: {e}")
    
    print("=" * 50)
    print("娴嬭瘯瀹屾垚")


if __name__ == "__main__":
    test_lexer())
        self.identifier_pattern = re.compile(r'^[\u4e00-\u9fffA-Za-z_][\u4e00-\u9fffA-Za-z0-9_]*
        灏嗘簮浠ｇ爜杞崲涓鸿瘝娉曞崟鍏冨垪琛?        
        Args:
            source_code: 婧愪唬鐮佸瓧绗︿覆
            
        Returns:
            璇嶆硶鍗曞厓鍒楄〃
        """
        tokens = []
        lines = source_code.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            line_tokens = self._tokenize_line(line, line_num)
            tokens.extend(line_tokens)
            
            # 娣诲姞鎹㈣绗︼紙闄ら潪鏄渶鍚庝竴琛岋級
            if line_num < len(lines):
                tokens.append(Token(TokenType.NEWLINE, '\n', line_num, len(line) + 1, '\n'))
        
        # 娣诲姞鏂囦欢缁撴潫鏍囪
        tokens.append(Token(TokenType.EOF, '', len(lines) + 1, 1, ''))
        
        return tokens
    
    def _tokenize_line(self, line: str, line_num: int) -> List[Token]:
        """灏嗕竴琛屼唬鐮佽浆鎹负璇嶆硶鍗曞厓鍒楄〃"""
        tokens = []
        position = 0
        column = 1
        
        # 浣跨敤鍒嗚瘝鍣ㄨ繘琛屼腑鏂囧垎璇?        segments = self._segment(line)
        segment_index = 0
        
        while position < len(line):
            # 璺宠繃绌虹櫧瀛楃
            if line[position].isspace():
                if line[position] == '\n':
                    tokens.append(Token(TokenType.NEWLINE, '\n', line_num, column, '\n'))
                position += 1
                column += 1
                continue
            
            # 澶勭悊娉ㄩ噴
            if line[position] == '#':
                # 鍗曡娉ㄩ噴锛岃烦杩囨暣琛?                comment = line[position:]
                tokens.append(Token(TokenType.COMMENT, comment, line_num, column, comment))
                break
            
            # 澶勭悊澶氳瑷€浠ｇ爜鍧?            if line[position:position+2] == '{{':
                tokens.append(Token(TokenType.CODE_BLOCK_START, '{{', line_num, column, '{{'))
                position += 2
                column += 2
                continue
            
            if line[position:position+2] == '}}':
                tokens.append(Token(TokenType.CODE_BLOCK_END, '}}', line_num, column, '}}'))
                position += 2
                column += 2
                continue
            
            # 澶勭悊涓枃鏍囩偣绗﹀彿
            if line[position] in self.chinese_punctuation:
                char = line[position]
                token_type = self.chinese_punctuation[char]
                
                # 澶勭悊鎴愬鏍囩偣绗﹀彿
                if char in ('銆?, '銆?):
                    # 鏌ユ壘鍖归厤鐨勭粨鏉熺鍙?                    end_pos = line.find('銆? if char == '銆? else '銆?, position + 1)
                    if end_pos != -1:
                        value = line[position:end_pos + 1]
                        tokens.append(Token(token_type, value, line_num, column, value))
                        position = end_pos + 1
                        column += len(value)
                        continue
                
                tokens.append(Token(token_type, char, line_num, column, char))
                position += 1
                column += 1
                continue
            
            # 澶勭悊鐪佺暐鍙?            if line[position:position+2] == '鈥︹€?:
                tokens.append(Token(TokenType.ELLIPSIS, '鈥︹€?, line_num, column, '鈥︹€?))
                position += 2
                column += 2
                continue
            
            # 澶勭悊鐮存姌鍙?            if line[position:position+2] == '鈥斺€?:
                tokens.append(Token(TokenType.DASH, '鈥斺€?, line_num, column, '鈥斺€?))
                position += 2
                column += 2
                continue
            
            # 澶勭悊鍦嗗湀鍙?            if line[position] in '鈶犫憽鈶⑩懀鈶も懃鈶︹懅鈶ㄢ懇':
                tokens.append(Token(TokenType.CIRCLED_NUMBERS, line[position], line_num, column, line[position]))
                position += 1
                column += 1
                continue
            
            # 澶勭悊杩愮畻绗?            if line[position] in self.operators:
                # 妫€鏌ュ弻瀛楃杩愮畻绗?                if position + 1 < len(line):
                    two_char = line[position:position+2]
                    if two_char in ('鈮?, '鈮?, '鈮?):
                        tokens.append(Token(self.operators[two_char], two_char, line_num, column, two_char))
                        position += 2
                        column += 2
                        continue
                
                tokens.append(Token(self.operators[line[position]], line[position], line_num, column, line[position]))
                position += 1
                column += 1
                continue
            
            # 澶勭悊鍒嗙粍绗﹀彿
            if line[position] in self.grouping_symbols:
                tokens.append(Token(self.grouping_symbols[line[position]], line[position], line_num, column, line[position]))
                position += 1
                column += 1
                continue
            
            # 澶勭悊瀛楃涓插瓧闈㈤噺
            if line[position] in ('"', "'"):
                string_token = self._parse_string_literal(line, position, line_num, column)
                tokens.append(string_token)
                position += len(string_token.lexeme)
                column += len(string_token.lexeme)
                continue
            
            # 澶勭悊鏁板瓧瀛楅潰閲?            if line[position].isdigit() or (line[position] == '.' and position + 1 < len(line) and line[position + 1].isdigit()):
                number_token = self._parse_number(line, position, line_num, column)
                tokens.append(number_token)
                position += len(number_token.lexeme)
                column += len(number_token.lexeme)
                continue
            
            # 澶勭悊涓枃鏁板瓧
            if line[position] in self.chinese_numbers:
                chinese_number_token = self._parse_chinese_number(line, position, line_num, column)
                tokens.append(chinese_number_token)
                position += len(chinese_number_token.lexeme)
                column += len(chinese_number_token.lexeme)
                continue
            
            # 澶勭悊褰撳墠鍒嗚瘝娈?            if segment_index < len(segments):
                segment = segments[segment_index].strip()
                if segment:  # 璺宠繃绌哄垎璇?                    # 澶勭悊鍒嗚瘝娈?                    token = self._process_segment(segment, line_num, column)
                    tokens.append(token)
                    position += len(segment)
                    column += len(segment)
                segment_index += 1
            else:
                # 濡傛灉娌℃湁鏇村鍒嗚瘝锛屽鐞嗗墿浣欏瓧绗?                identifier_token = self._parse_identifier(line, position, line_num, column)
                tokens.append(identifier_token)
                position += len(identifier_token.lexeme)
                column += len(identifier_token.lexeme)
        
        return tokens
    
    def _process_segment(self, segment: str, line_num: int, column: int) -> Token:
        """澶勭悊鍒嗚瘝娈?""
        # 妫€鏌ユ槸鍚︿负鍏抽敭璇?        token_type = self._get_keyword_type(segment)
        if token_type:
            return Token(token_type, segment, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负鐧惧濮撳彉閲?        if self._is_bai_jia_xing(segment):
            return Token(TokenType.BAIJIAXING, segment, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负鍔ㄨ瘝
        arity = get_verb_arity(segment)
        if arity != 0:
            # 鏍规嵁鍏冩暟纭畾鍔ㄨ瘝绫诲瀷
            if arity == -1:
                token_type = TokenType.VERB_VAR
            elif arity == 0:
                token_type = TokenType.VERB_0
            elif arity == 1:
                token_type = TokenType.VERB_1
            elif arity == 2:
                token_type = TokenType.VERB_2
            elif arity == 3:
                token_type = TokenType.VERB_3
            else:
                token_type = TokenType.VERB_VAR
            
            return Token(token_type, segment, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负甯冨皵瀛楅潰閲?        if segment in ('鐪?, '鍋?, 'true', 'false', 'True', 'False'):
            value = segment in ('鐪?, 'true', 'True')
            return Token(TokenType.BOOLEAN, value, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负绌哄€?        if segment == '绌?:
            return Token(TokenType.NULL, None, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负鏁板瓧
        if segment.isdigit() or (segment.replace('.', '', 1).isdigit() and segment.count('.') == 1):
            try:
                if '.' in segment:
                    value = float(segment)
                else:
                    value = int(segment)
                return Token(TokenType.NUMBER, value, line_num, column, segment)
            except ValueError:
                pass
        
        # 妫€鏌ユ槸鍚︿负涓枃鏁板瓧
        if all(c in self.chinese_numbers for c in segment):
            value = self._chinese_to_arabic(segment)
            return Token(TokenType.CHINESE_NUMBER, value, line_num, column, segment)
        
        # 鏅€氭爣璇嗙
        return Token(TokenType.IDENTIFIER, segment, line_num, column, segment)
    
    def _parse_string_literal(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽瀛楃涓插瓧闈㈤噺"""
        quote_char = line[start]
        position = start + 1
        value = ''
        
        while position < len(line):
            char = line[position]
            
            if char == quote_char:
                # 缁撴潫寮曞彿
                position += 1
                break
            elif char == '\\' and position + 1 < len(line):
                # 杞箟瀛楃
                next_char = line[position + 1]
                if next_char in ('n', 't', '\\', '"', "'"):
                    value += self._escape_char(next_char)
                    position += 2
                else:
                    value += char
                    position += 1
            else:
                value += char
                position += 1
        
        lexeme = line[start:position]
        return Token(TokenType.STRING, value, line_num, column, lexeme)
    
    def _escape_char(self, char: str) -> str:
        """杞箟瀛楃"""
        escape_map = {
            'n': '\n',
            't': '\t',
            '\\': '\\',
            '"': '"',
            "'": "'",
        }
        return escape_map.get(char, char)
    
    def _parse_number(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽鏁板瓧瀛楅潰閲?""
        position = start
        
        # 瑙ｆ瀽鏁存暟閮ㄥ垎
        while position < len(line) and line[position].isdigit():
            position += 1
        
        # 瑙ｆ瀽灏忔暟閮ㄥ垎
        if position < len(line) and line[position] == '.':
            position += 1
            while position < len(line) and line[position].isdigit():
                position += 1
        
        # 瑙ｆ瀽绉戝璁℃暟娉?        if position < len(line) and line[position].lower() == 'e':
            position += 1
            if position < len(line) and line[position] in ('+', '-'):
                position += 1
            while position < len(line) and line[position].isdigit():
                position += 1
        
        lexeme = line[start:position]
        
        # 灏濊瘯杞崲涓烘暟瀛?        try:
            if '.' in lexeme or 'e' in lexeme.lower():
                value = float(lexeme)
            else:
                value = int(lexeme)
        except ValueError:
            value = lexeme  # 淇濇寔鍘熸牱
        
        return Token(TokenType.NUMBER, value, line_num, column, lexeme)
    
    def _parse_chinese_number(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽涓枃鏁板瓧"""
        position = start
        lexeme = ''
        
        while position < len(line) and line[position] in self.chinese_numbers:
            lexeme += line[position]
            position += 1
        
        # 杞崲涓洪樋鎷変集鏁板瓧
        value = self._chinese_to_arabic(lexeme)
        
        return Token(TokenType.CHINESE_NUMBER, value, line_num, column, lexeme)
    
    def _chinese_to_arabic(self, chinese_num: str) -> int:
        """灏嗕腑鏂囨暟瀛楄浆鎹负闃挎媺浼暟瀛?""
        if not chinese_num:
            return 0
        
        # 绠€鍗曞疄鐜帮紝鍙鐞嗗熀鏈暟瀛?        total = 0
        current = 0
        
        for char in chinese_num:
            num = self.chinese_numbers.get(char, 0)
            
            if num < 10:
                current = num
            elif num >= 10:
                if current == 0:
                    current = 1
                total += current * num
                current = 0
        
        total += current
        return total
    
    def _parse_identifier(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽鏍囪瘑绗?""
        position = start
        
        # 鏀堕泦鏍囪瘑绗﹀瓧绗?        while position < len(line) and self._is_identifier_char(line[position]):
            position += 1
        
        lexeme = line[start:position]
        
        # 妫€鏌ユ槸鍚︿负鍏抽敭璇?        token_type = self._get_keyword_type(lexeme)
        if token_type:
            return Token(token_type, lexeme, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负鐧惧濮撳彉閲?        if self._is_bai_jia_xing(lexeme):
            return Token(TokenType.BAIJIAXING, lexeme, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负鍔ㄨ瘝
        arity = get_verb_arity(lexeme)
        if arity != 0:
            # 鏍规嵁鍏冩暟纭畾鍔ㄨ瘝绫诲瀷
            if arity == -1:
                token_type = TokenType.VERB_VAR
            elif arity == 0:
                token_type = TokenType.VERB_0
            elif arity == 1:
                token_type = TokenType.VERB_1
            elif arity == 2:
                token_type = TokenType.VERB_2
            elif arity == 3:
                token_type = TokenType.VERB_3
            else:
                token_type = TokenType.VERB_VAR
            
            return Token(token_type, lexeme, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负甯冨皵瀛楅潰閲?        if lexeme in ('鐪?, '鍋?, 'true', 'false', 'True', 'False'):
            value = lexeme in ('鐪?, 'true', 'True')
            return Token(TokenType.BOOLEAN, value, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负绌哄€?        if lexeme == '绌?:
            return Token(TokenType.NULL, None, line_num, column, lexeme)
        
        # 灏濊瘯涓枃鍒嗚瘝
        if len(lexeme) > 1 and any('\u4e00' <= c <= '\u9fff' for c in lexeme):
            # 浣跨敤jieba杩涜涓枃鍒嗚瘝
            segments = self._segment(lexeme)
            if len(segments) > 1:
                # 濡傛灉鏄涓瘝锛岃繑鍥炵涓€涓瘝浣滀负鏍囪瘑绗?                first_segment = segments[0]
                # 閫掑綊澶勭悊绗竴涓瘝
                return self._parse_identifier(first_segment, 0, line_num, column)
        
        # 鏅€氭爣璇嗙
        return Token(TokenType.IDENTIFIER, lexeme, line_num, column, lexeme)
    
    def _is_identifier_char(self, char: str) -> bool:
        """妫€鏌ュ瓧绗︽槸鍚︿负鏍囪瘑绗﹀瓧绗?""
        # 涓枃瀛楃銆佽嫳鏂囧瓧姣嶃€佹暟瀛椼€佷笅鍒掔嚎
        return ('\u4e00' <= char <= '\u9fff' or
                'a' <= char <= 'z' or
                'A' <= char <= 'Z' or
                char.isdigit() or
                char == '_')
    
    def _get_keyword_type(self, lexeme: str) -> Optional[TokenType]:
        """鑾峰彇鍏抽敭璇嶇被鍨?""
        # 妫€鏌ョ姸鎬佸叧閿瘝锛堝瀛楋級
        for keyword, token_type in self.state_keywords.items():
            if lexeme.startswith(keyword):
                return token_type
        
        # 妫€鏌ユ劅鐭ュ叧閿瘝锛堝瀛楋級
        for keyword, token_type in self.perception_keywords.items():
            if lexeme.startswith(keyword):
                return token_type
        
        # 妫€鏌ユ椂闂村叧閿瘝锛堝瀛楋級
        for keyword, token_type in self.time_keywords.items():
            if lexeme.startswith(keyword):
                return token_type
        
        # 妫€鏌ユ櫘閫氬叧閿瘝
        return self.keywords.get(lexeme)
    
    def _is_bai_jia_xing(self, lexeme: str) -> bool:
        """妫€鏌ユ槸鍚︿负鐧惧濮撳彉閲?""
        if not lexeme:
            return False
        
        # 鑾峰彇濮撴皬锛堢涓€涓瓧绗︼級
        surname = lexeme[0]
        
        # 妫€鏌ユ槸鍚︿负鍐茬獊濮撴皬
        if surname in self.conflict_surnames:
            return False
        
        # 妫€鏌ユ槸鍚︿负鐧惧濮?        return surname in self.bai_jia_xing
    
    def print_tokens(self, tokens: List[Token]) -> None:
        """鎵撳嵃璇嶆硶鍗曞厓鍒楄〃"""
        print("璇嶆硶鍒嗘瀽缁撴灉:")
        print("=" * 80)
        print(f"{'琛?:<4} {'鍒?:<4} {'绫诲瀷':<20} {'鍊?:<20} {'璇嶇礌':<20}")
        print("-" * 80)
        
        for token in tokens:
            value_str = str(token.value)
            if len(value_str) > 18:
                value_str = value_str[:15] + "..."
            
            lexeme_str = token.lexeme
            if len(lexeme_str) > 18:
                lexeme_str = lexeme_str[:15] + "..."
            
            print(f"{token.line:<4} {token.column:<4} {token.type.value:<20} {value_str:<20} {lexeme_str:<20}")
        
        print("=" * 80)


# 娴嬭瘯鍑芥暟
def test_lexer():
    """娴嬭瘯璇嶆硶鍒嗘瀽鍣?""
    print("璇嶆硶鍒嗘瀽鍣ㄦ祴璇?)
    print("=" * 50)
    
    lexer = YanLuLexer()
    
    # 娴嬭瘯鐢ㄤ緥
    test_cases = [
        (
            "瀹氭俯搴︽槸25銆?,
            "鍙橀噺瀹氫箟"
        ),
        (
            "濡傛灉娓╁害澶?0灏卞紑鍚鎵囥€?,
            "鏉′欢璇彞"
        ),
        (
            "瀵逛簬i鍦?鍒?0锛氬嵃i銆?,
            "寰幆璇彞"
        ),
        (
            "娓╁害鍙樹负30搴︺€?,
            "鐘舵€佽浆鎹?
        ),
        (
            "寮犱笁銆佹潕鍥涳紝璁＄畻鎶樻墸銆?,
            "鎰忓悎寮忓嚱鏁拌皟鐢?
        ),
        (
            "'浣犲ソ锛屼笘鐣?",
            "瀛楃涓插瓧闈㈤噺"
        ),
        (
            "鐪熶笖鍋?,
            "甯冨皵杩愮畻"
        ),
        (
            "瀹歺绛変簬鍗佸姞浜斻€?,
            "涓枃鏁板瓧"
        ),
    ]
    
    for source_code, description in test_cases:
        print(f"\n娴嬭瘯: {description}")
        print(f"婧愪唬鐮? {source_code}")
        
        try:
            tokens = lexer.tokenize(source_code)
            lexer.print_tokens(tokens)
        except Exception as e:
            print(f"閿欒: {e}")
    
    print("=" * 50)
    print("娴嬭瘯瀹屾垚")


if __name__ == "__main__":
    test_lexer())
        self.identifier_pattern = re.compile(r'^[\u4e00-\u9fffA-Za-z_][\u4e00-\u9fffA-Za-z0-9_]*
        """
        灏嗘簮浠ｇ爜杞崲涓鸿瘝娉曞崟鍏冨垪琛?        
        Args:
            source_code: 婧愪唬鐮佸瓧绗︿覆
            
        Returns:
            璇嶆硶鍗曞厓鍒楄〃
        """
        tokens = []
        lines = source_code.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            line_tokens = self._tokenize_line(line, line_num)
            tokens.extend(line_tokens)
            
            # 娣诲姞鎹㈣绗︼紙闄ら潪鏄渶鍚庝竴琛岋級
            if line_num < len(lines):
                tokens.append(Token(TokenType.NEWLINE, '\n', line_num, len(line) + 1, '\n'))
        
        # 娣诲姞鏂囦欢缁撴潫鏍囪
        tokens.append(Token(TokenType.EOF, '', len(lines) + 1, 1, ''))
        
        return tokens
    
    def _tokenize_line(self, line: str, line_num: int) -> List[Token]:
        """灏嗕竴琛屼唬鐮佽浆鎹负璇嶆硶鍗曞厓鍒楄〃"""
        tokens = []
        position = 0
        column = 1
        
        # 浣跨敤鍒嗚瘝鍣ㄨ繘琛屼腑鏂囧垎璇?        segments = self._segment(line)
        segment_index = 0
        
        while position < len(line):
            # 璺宠繃绌虹櫧瀛楃
            if line[position].isspace():
                if line[position] == '\n':
                    tokens.append(Token(TokenType.NEWLINE, '\n', line_num, column, '\n'))
                position += 1
                column += 1
                continue
            
            # 澶勭悊娉ㄩ噴
            if line[position] == '#':
                # 鍗曡娉ㄩ噴锛岃烦杩囨暣琛?                comment = line[position:]
                tokens.append(Token(TokenType.COMMENT, comment, line_num, column, comment))
                break
            
            # 澶勭悊澶氳瑷€浠ｇ爜鍧?            if line[position:position+2] == '{{':
                tokens.append(Token(TokenType.CODE_BLOCK_START, '{{', line_num, column, '{{'))
                position += 2
                column += 2
                continue
            
            if line[position:position+2] == '}}':
                tokens.append(Token(TokenType.CODE_BLOCK_END, '}}', line_num, column, '}}'))
                position += 2
                column += 2
                continue
            
            # 澶勭悊涓枃鏍囩偣绗﹀彿
            if line[position] in self.chinese_punctuation:
                char = line[position]
                token_type = self.chinese_punctuation[char]
                
                # 澶勭悊鎴愬鏍囩偣绗﹀彿
                if char in ('銆?, '銆?):
                    # 鏌ユ壘鍖归厤鐨勭粨鏉熺鍙?                    end_pos = line.find('銆? if char == '銆? else '銆?, position + 1)
                    if end_pos != -1:
                        value = line[position:end_pos + 1]
                        tokens.append(Token(token_type, value, line_num, column, value))
                        position = end_pos + 1
                        column += len(value)
                        continue
                
                tokens.append(Token(token_type, char, line_num, column, char))
                position += 1
                column += 1
                continue
            
            # 澶勭悊鐪佺暐鍙?            if line[position:position+2] == '鈥︹€?:
                tokens.append(Token(TokenType.ELLIPSIS, '鈥︹€?, line_num, column, '鈥︹€?))
                position += 2
                column += 2
                continue
            
            # 澶勭悊鐮存姌鍙?            if line[position:position+2] == '鈥斺€?:
                tokens.append(Token(TokenType.DASH, '鈥斺€?, line_num, column, '鈥斺€?))
                position += 2
                column += 2
                continue
            
            # 澶勭悊鍦嗗湀鍙?            if line[position] in '鈶犫憽鈶⑩懀鈶も懃鈶︹懅鈶ㄢ懇':
                tokens.append(Token(TokenType.CIRCLED_NUMBERS, line[position], line_num, column, line[position]))
                position += 1
                column += 1
                continue
            
            # 澶勭悊杩愮畻绗?            if line[position] in self.operators:
                # 妫€鏌ュ弻瀛楃杩愮畻绗?                if position + 1 < len(line):
                    two_char = line[position:position+2]
                    if two_char in ('鈮?, '鈮?, '鈮?):
                        tokens.append(Token(self.operators[two_char], two_char, line_num, column, two_char))
                        position += 2
                        column += 2
                        continue
                
                tokens.append(Token(self.operators[line[position]], line[position], line_num, column, line[position]))
                position += 1
                column += 1
                continue
            
            # 澶勭悊鍒嗙粍绗﹀彿
            if line[position] in self.grouping_symbols:
                tokens.append(Token(self.grouping_symbols[line[position]], line[position], line_num, column, line[position]))
                position += 1
                column += 1
                continue
            
            # 澶勭悊瀛楃涓插瓧闈㈤噺
            if line[position] in ('"', "'"):
                string_token = self._parse_string_literal(line, position, line_num, column)
                tokens.append(string_token)
                position += len(string_token.lexeme)
                column += len(string_token.lexeme)
                continue
            
            # 澶勭悊鏁板瓧瀛楅潰閲?            if line[position].isdigit() or (line[position] == '.' and position + 1 < len(line) and line[position + 1].isdigit()):
                number_token = self._parse_number(line, position, line_num, column)
                tokens.append(number_token)
                position += len(number_token.lexeme)
                column += len(number_token.lexeme)
                continue
            
            # 澶勭悊涓枃鏁板瓧
            if line[position] in self.chinese_numbers:
                chinese_number_token = self._parse_chinese_number(line, position, line_num, column)
                tokens.append(chinese_number_token)
                position += len(chinese_number_token.lexeme)
                column += len(chinese_number_token.lexeme)
                continue
            
            # 澶勭悊褰撳墠鍒嗚瘝娈?            if segment_index < len(segments):
                segment = segments[segment_index].strip()
                if segment:  # 璺宠繃绌哄垎璇?                    # 澶勭悊鍒嗚瘝娈?                    token = self._process_segment(segment, line_num, column)
                    tokens.append(token)
                    position += len(segment)
                    column += len(segment)
                segment_index += 1
            else:
                # 濡傛灉娌℃湁鏇村鍒嗚瘝锛屽鐞嗗墿浣欏瓧绗?                identifier_token = self._parse_identifier(line, position, line_num, column)
                tokens.append(identifier_token)
                position += len(identifier_token.lexeme)
                column += len(identifier_token.lexeme)
        
        return tokens
    
    def _process_segment(self, segment: str, line_num: int, column: int) -> Token:
        """澶勭悊鍒嗚瘝娈?""
        # 妫€鏌ユ槸鍚︿负鍏抽敭璇?        token_type = self._get_keyword_type(segment)
        if token_type:
            return Token(token_type, segment, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负鐧惧濮撳彉閲?        if self._is_bai_jia_xing(segment):
            return Token(TokenType.BAIJIAXING, segment, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负鍔ㄨ瘝
        arity = get_verb_arity(segment)
        if arity != 0:
            # 鏍规嵁鍏冩暟纭畾鍔ㄨ瘝绫诲瀷
            if arity == -1:
                token_type = TokenType.VERB_VAR
            elif arity == 0:
                token_type = TokenType.VERB_0
            elif arity == 1:
                token_type = TokenType.VERB_1
            elif arity == 2:
                token_type = TokenType.VERB_2
            elif arity == 3:
                token_type = TokenType.VERB_3
            else:
                token_type = TokenType.VERB_VAR
            
            return Token(token_type, segment, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负甯冨皵瀛楅潰閲?        if segment in ('鐪?, '鍋?, 'true', 'false', 'True', 'False'):
            value = segment in ('鐪?, 'true', 'True')
            return Token(TokenType.BOOLEAN, value, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负绌哄€?        if segment == '绌?:
            return Token(TokenType.NULL, None, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负鏁板瓧
        if segment.isdigit() or (segment.replace('.', '', 1).isdigit() and segment.count('.') == 1):
            try:
                if '.' in segment:
                    value = float(segment)
                else:
                    value = int(segment)
                return Token(TokenType.NUMBER, value, line_num, column, segment)
            except ValueError:
                pass
        
        # 妫€鏌ユ槸鍚︿负涓枃鏁板瓧
        if all(c in self.chinese_numbers for c in segment):
            value = self._chinese_to_arabic(segment)
            return Token(TokenType.CHINESE_NUMBER, value, line_num, column, segment)
        
        # 鏅€氭爣璇嗙
        return Token(TokenType.IDENTIFIER, segment, line_num, column, segment)
    
    def _parse_string_literal(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽瀛楃涓插瓧闈㈤噺"""
        quote_char = line[start]
        position = start + 1
        value = ''
        
        while position < len(line):
            char = line[position]
            
            if char == quote_char:
                # 缁撴潫寮曞彿
                position += 1
                break
            elif char == '\\' and position + 1 < len(line):
                # 杞箟瀛楃
                next_char = line[position + 1]
                if next_char in ('n', 't', '\\', '"', "'"):
                    value += self._escape_char(next_char)
                    position += 2
                else:
                    value += char
                    position += 1
            else:
                value += char
                position += 1
        
        lexeme = line[start:position]
        return Token(TokenType.STRING, value, line_num, column, lexeme)
    
    def _escape_char(self, char: str) -> str:
        """杞箟瀛楃"""
        escape_map = {
            'n': '\n',
            't': '\t',
            '\\': '\\',
            '"': '"',
            "'": "'",
        }
        return escape_map.get(char, char)
    
    def _parse_number(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽鏁板瓧瀛楅潰閲?""
        position = start
        
        # 瑙ｆ瀽鏁存暟閮ㄥ垎
        while position < len(line) and line[position].isdigit():
            position += 1
        
        # 瑙ｆ瀽灏忔暟閮ㄥ垎
        if position < len(line) and line[position] == '.':
            position += 1
            while position < len(line) and line[position].isdigit():
                position += 1
        
        # 瑙ｆ瀽绉戝璁℃暟娉?        if position < len(line) and line[position].lower() == 'e':
            position += 1
            if position < len(line) and line[position] in ('+', '-'):
                position += 1
            while position < len(line) and line[position].isdigit():
                position += 1
        
        lexeme = line[start:position]
        
        # 灏濊瘯杞崲涓烘暟瀛?        try:
            if '.' in lexeme or 'e' in lexeme.lower():
                value = float(lexeme)
            else:
                value = int(lexeme)
        except ValueError:
            value = lexeme  # 淇濇寔鍘熸牱
        
        return Token(TokenType.NUMBER, value, line_num, column, lexeme)
    
    def _parse_chinese_number(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽涓枃鏁板瓧"""
        position = start
        lexeme = ''
        
        while position < len(line) and line[position] in self.chinese_numbers:
            lexeme += line[position]
            position += 1
        
        # 杞崲涓洪樋鎷変集鏁板瓧
        value = self._chinese_to_arabic(lexeme)
        
        return Token(TokenType.CHINESE_NUMBER, value, line_num, column, lexeme)
    
    def _chinese_to_arabic(self, chinese_num: str) -> int:
        """灏嗕腑鏂囨暟瀛楄浆鎹负闃挎媺浼暟瀛?""
        if not chinese_num:
            return 0
        
        # 绠€鍗曞疄鐜帮紝鍙鐞嗗熀鏈暟瀛?        total = 0
        current = 0
        
        for char in chinese_num:
            num = self.chinese_numbers.get(char, 0)
            
            if num < 10:
                current = num
            elif num >= 10:
                if current == 0:
                    current = 1
                total += current * num
                current = 0
        
        total += current
        return total
    
    def _parse_identifier(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽鏍囪瘑绗?""
        position = start
        
        # 鏀堕泦鏍囪瘑绗﹀瓧绗?        while position < len(line) and self._is_identifier_char(line[position]):
            position += 1
        
        lexeme = line[start:position]
        
        # 妫€鏌ユ槸鍚︿负鍏抽敭璇?        token_type = self._get_keyword_type(lexeme)
        if token_type:
            return Token(token_type, lexeme, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负鐧惧濮撳彉閲?        if self._is_bai_jia_xing(lexeme):
            return Token(TokenType.BAIJIAXING, lexeme, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负鍔ㄨ瘝
        arity = get_verb_arity(lexeme)
        if arity != 0:
            # 鏍规嵁鍏冩暟纭畾鍔ㄨ瘝绫诲瀷
            if arity == -1:
                token_type = TokenType.VERB_VAR
            elif arity == 0:
                token_type = TokenType.VERB_0
            elif arity == 1:
                token_type = TokenType.VERB_1
            elif arity == 2:
                token_type = TokenType.VERB_2
            elif arity == 3:
                token_type = TokenType.VERB_3
            else:
                token_type = TokenType.VERB_VAR
            
            return Token(token_type, lexeme, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负甯冨皵瀛楅潰閲?        if lexeme in ('鐪?, '鍋?, 'true', 'false', 'True', 'False'):
            value = lexeme in ('鐪?, 'true', 'True')
            return Token(TokenType.BOOLEAN, value, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负绌哄€?        if lexeme == '绌?:
            return Token(TokenType.NULL, None, line_num, column, lexeme)
        
        # 灏濊瘯涓枃鍒嗚瘝
        if len(lexeme) > 1 and any('\u4e00' <= c <= '\u9fff' for c in lexeme):
            # 浣跨敤jieba杩涜涓枃鍒嗚瘝
            segments = self._segment(lexeme)
            if len(segments) > 1:
                # 濡傛灉鏄涓瘝锛岃繑鍥炵涓€涓瘝浣滀负鏍囪瘑绗?                first_segment = segments[0]
                # 閫掑綊澶勭悊绗竴涓瘝
                return self._parse_identifier(first_segment, 0, line_num, column)
        
        # 鏅€氭爣璇嗙
        return Token(TokenType.IDENTIFIER, lexeme, line_num, column, lexeme)
    
    def _is_identifier_char(self, char: str) -> bool:
        """妫€鏌ュ瓧绗︽槸鍚︿负鏍囪瘑绗﹀瓧绗?""
        # 涓枃瀛楃銆佽嫳鏂囧瓧姣嶃€佹暟瀛椼€佷笅鍒掔嚎
        return ('\u4e00' <= char <= '\u9fff' or
                'a' <= char <= 'z' or
                'A' <= char <= 'Z' or
                char.isdigit() or
                char == '_')
    
    def _get_keyword_type(self, lexeme: str) -> Optional[TokenType]:
        """鑾峰彇鍏抽敭璇嶇被鍨?""
        # 妫€鏌ョ姸鎬佸叧閿瘝锛堝瀛楋級
        for keyword, token_type in self.state_keywords.items():
            if lexeme.startswith(keyword):
                return token_type
        
        # 妫€鏌ユ劅鐭ュ叧閿瘝锛堝瀛楋級
        for keyword, token_type in self.perception_keywords.items():
            if lexeme.startswith(keyword):
                return token_type
        
        # 妫€鏌ユ椂闂村叧閿瘝锛堝瀛楋級
        for keyword, token_type in self.time_keywords.items():
            if lexeme.startswith(keyword):
                return token_type
        
        # 妫€鏌ユ櫘閫氬叧閿瘝
        return self.keywords.get(lexeme)
    
    def _is_bai_jia_xing(self, lexeme: str) -> bool:
        """妫€鏌ユ槸鍚︿负鐧惧濮撳彉閲?""
        if not lexeme:
            return False
        
        # 鑾峰彇濮撴皬锛堢涓€涓瓧绗︼級
        surname = lexeme[0]
        
        # 妫€鏌ユ槸鍚︿负鍐茬獊濮撴皬
        if surname in self.conflict_surnames:
            return False
        
        # 妫€鏌ユ槸鍚︿负鐧惧濮?        return surname in self.bai_jia_xing
    
    def print_tokens(self, tokens: List[Token]) -> None:
        """鎵撳嵃璇嶆硶鍗曞厓鍒楄〃"""
        print("璇嶆硶鍒嗘瀽缁撴灉:")
        print("=" * 80)
        print(f"{'琛?:<4} {'鍒?:<4} {'绫诲瀷':<20} {'鍊?:<20} {'璇嶇礌':<20}")
        print("-" * 80)
        
        for token in tokens:
            value_str = str(token.value)
            if len(value_str) > 18:
                value_str = value_str[:15] + "..."
            
            lexeme_str = token.lexeme
            if len(lexeme_str) > 18:
                lexeme_str = lexeme_str[:15] + "..."
            
            print(f"{token.line:<4} {token.column:<4} {token.type.value:<20} {value_str:<20} {lexeme_str:<20}")
        
        print("=" * 80)


# 娴嬭瘯鍑芥暟
def test_lexer():
    """娴嬭瘯璇嶆硶鍒嗘瀽鍣?""
    print("璇嶆硶鍒嗘瀽鍣ㄦ祴璇?)
    print("=" * 50)
    
    lexer = YanLuLexer()
    
    # 娴嬭瘯鐢ㄤ緥
    test_cases = [
        (
            "瀹氭俯搴︽槸25銆?,
            "鍙橀噺瀹氫箟"
        ),
        (
            "濡傛灉娓╁害澶?0灏卞紑鍚鎵囥€?,
            "鏉′欢璇彞"
        ),
        (
            "瀵逛簬i鍦?鍒?0锛氬嵃i銆?,
            "寰幆璇彞"
        ),
        (
            "娓╁害鍙樹负30搴︺€?,
            "鐘舵€佽浆鎹?
        ),
        (
            "寮犱笁銆佹潕鍥涳紝璁＄畻鎶樻墸銆?,
            "鎰忓悎寮忓嚱鏁拌皟鐢?
        ),
        (
            "'浣犲ソ锛屼笘鐣?",
            "瀛楃涓插瓧闈㈤噺"
        ),
        (
            "鐪熶笖鍋?,
            "甯冨皵杩愮畻"
        ),
        (
            "瀹歺绛変簬鍗佸姞浜斻€?,
            "涓枃鏁板瓧"
        ),
    ]
    
    for source_code, description in test_cases:
        print(f"\n娴嬭瘯: {description}")
        print(f"婧愪唬鐮? {source_code}")
        
        try:
            tokens = lexer.tokenize(source_code)
            lexer.print_tokens(tokens)
        except Exception as e:
            print(f"閿欒: {e}")
    
    print("=" * 50)
    print("娴嬭瘯瀹屾垚")


if __name__ == "__main__":
    test_lexer())
    
    def _init_segmenter(self):
        """鍒濆鍖栧垎璇嶅櫒"""
        if self.segmenter_type == "thulac":
            try:
                import thulac
                # 浣跨敤seg_only=True鍙繘琛屽垎璇嶏紝涓嶈繘琛岃瘝鎬ф爣娉?                self.segmenter = thulac.thulac(seg_only=True, model_path=None)
                print(f"浣跨敤THULAC鍒嗚瘝鍣?(seg_only妯″紡)")
            except ImportError:
                print("璀﹀憡: 鏈畨瑁匱HULAC锛屽洖閫€鍒癹ieba鍒嗚瘝鍣?)
                print("瀹夎鍛戒护: pip install thulac")
                self.segmenter_type = "jieba"
                self.segmenter = jieba
        else:
            # 榛樿浣跨敤jieba
            self.segmenter = jieba
            print(f"浣跨敤jieba鍒嗚瘝鍣?)
    
    def _segment(self, text: str) -> List[str]:
        """
        鍒嗚瘝鏂规硶
        
        Args:
            text: 寰呭垎璇嶇殑鏂囨湰
            
        Returns:
            鍒嗚瘝缁撴灉鍒楄〃
        """
        if self.segmenter_type == "thulac":
            # THULAC鍒嗚瘝
            result = self.segmenter.cut(text, text=True)
            return result.split()
        else:
            # jieba鍒嗚瘝
            return list(self.segmenter.lcut(text))
        
    def tokenize(self, source_code: str) -> List[Token]:
        """
        灏嗘簮浠ｇ爜杞崲涓鸿瘝娉曞崟鍏冨垪琛?        
        Args:
            source_code: 婧愪唬鐮佸瓧绗︿覆
            
        Returns:
            璇嶆硶鍗曞厓鍒楄〃
        """
        tokens = []
        lines = source_code.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            line_tokens = self._tokenize_line(line, line_num)
            tokens.extend(line_tokens)
            
            # 娣诲姞鎹㈣绗︼紙闄ら潪鏄渶鍚庝竴琛岋級
            if line_num < len(lines):
                tokens.append(Token(TokenType.NEWLINE, '\n', line_num, len(line) + 1, '\n'))
        
        # 娣诲姞鏂囦欢缁撴潫鏍囪
        tokens.append(Token(TokenType.EOF, '', len(lines) + 1, 1, ''))
        
        return tokens
    
    def _tokenize_line(self, line: str, line_num: int) -> List[Token]:
        """灏嗕竴琛屼唬鐮佽浆鎹负璇嶆硶鍗曞厓鍒楄〃"""
        tokens = []
        position = 0
        column = 1
        
        # 浣跨敤鍒嗚瘝鍣ㄨ繘琛屼腑鏂囧垎璇?        segments = self._segment(line)
        segment_index = 0
        
        while position < len(line):
            # 璺宠繃绌虹櫧瀛楃
            if line[position].isspace():
                if line[position] == '\n':
                    tokens.append(Token(TokenType.NEWLINE, '\n', line_num, column, '\n'))
                position += 1
                column += 1
                continue
            
            # 澶勭悊娉ㄩ噴
            if line[position] == '#':
                # 鍗曡娉ㄩ噴锛岃烦杩囨暣琛?                comment = line[position:]
                tokens.append(Token(TokenType.COMMENT, comment, line_num, column, comment))
                break
            
            # 澶勭悊澶氳瑷€浠ｇ爜鍧?            if line[position:position+2] == '{{':
                tokens.append(Token(TokenType.CODE_BLOCK_START, '{{', line_num, column, '{{'))
                position += 2
                column += 2
                continue
            
            if line[position:position+2] == '}}':
                tokens.append(Token(TokenType.CODE_BLOCK_END, '}}', line_num, column, '}}'))
                position += 2
                column += 2
                continue
            
            # 澶勭悊涓枃鏍囩偣绗﹀彿
            if line[position] in self.chinese_punctuation:
                char = line[position]
                token_type = self.chinese_punctuation[char]
                
                # 澶勭悊鎴愬鏍囩偣绗﹀彿
                if char in ('銆?, '銆?):
                    # 鏌ユ壘鍖归厤鐨勭粨鏉熺鍙?                    end_pos = line.find('銆? if char == '銆? else '銆?, position + 1)
                    if end_pos != -1:
                        value = line[position:end_pos + 1]
                        tokens.append(Token(token_type, value, line_num, column, value))
                        position = end_pos + 1
                        column += len(value)
                        continue
                
                tokens.append(Token(token_type, char, line_num, column, char))
                position += 1
                column += 1
                continue
            
            # 澶勭悊鐪佺暐鍙?            if line[position:position+2] == '鈥︹€?:
                tokens.append(Token(TokenType.ELLIPSIS, '鈥︹€?, line_num, column, '鈥︹€?))
                position += 2
                column += 2
                continue
            
            # 澶勭悊鐮存姌鍙?            if line[position:position+2] == '鈥斺€?:
                tokens.append(Token(TokenType.DASH, '鈥斺€?, line_num, column, '鈥斺€?))
                position += 2
                column += 2
                continue
            
            # 澶勭悊鍦嗗湀鍙?            if line[position] in '鈶犫憽鈶⑩懀鈶も懃鈶︹懅鈶ㄢ懇':
                tokens.append(Token(TokenType.CIRCLED_NUMBERS, line[position], line_num, column, line[position]))
                position += 1
                column += 1
                continue
            
            # 澶勭悊杩愮畻绗?            if line[position] in self.operators:
                # 妫€鏌ュ弻瀛楃杩愮畻绗?                if position + 1 < len(line):
                    two_char = line[position:position+2]
                    if two_char in ('鈮?, '鈮?, '鈮?):
                        tokens.append(Token(self.operators[two_char], two_char, line_num, column, two_char))
                        position += 2
                        column += 2
                        continue
                
                tokens.append(Token(self.operators[line[position]], line[position], line_num, column, line[position]))
                position += 1
                column += 1
                continue
            
            # 澶勭悊鍒嗙粍绗﹀彿
            if line[position] in self.grouping_symbols:
                tokens.append(Token(self.grouping_symbols[line[position]], line[position], line_num, column, line[position]))
                position += 1
                column += 1
                continue
            
            # 澶勭悊瀛楃涓插瓧闈㈤噺
            if line[position] in ('"', "'"):
                string_token = self._parse_string_literal(line, position, line_num, column)
                tokens.append(string_token)
                position += len(string_token.lexeme)
                column += len(string_token.lexeme)
                continue
            
            # 澶勭悊鏁板瓧瀛楅潰閲?            if line[position].isdigit() or (line[position] == '.' and position + 1 < len(line) and line[position + 1].isdigit()):
                number_token = self._parse_number(line, position, line_num, column)
                tokens.append(number_token)
                position += len(number_token.lexeme)
                column += len(number_token.lexeme)
                continue
            
            # 澶勭悊涓枃鏁板瓧
            if line[position] in self.chinese_numbers:
                chinese_number_token = self._parse_chinese_number(line, position, line_num, column)
                tokens.append(chinese_number_token)
                position += len(chinese_number_token.lexeme)
                column += len(chinese_number_token.lexeme)
                continue
            
            # 澶勭悊褰撳墠鍒嗚瘝娈?            if segment_index < len(segments):
                segment = segments[segment_index].strip()
                if segment:  # 璺宠繃绌哄垎璇?                    # 澶勭悊鍒嗚瘝娈?                    token = self._process_segment(segment, line_num, column)
                    tokens.append(token)
                    position += len(segment)
                    column += len(segment)
                segment_index += 1
            else:
                # 濡傛灉娌℃湁鏇村鍒嗚瘝锛屽鐞嗗墿浣欏瓧绗?                identifier_token = self._parse_identifier(line, position, line_num, column)
                tokens.append(identifier_token)
                position += len(identifier_token.lexeme)
                column += len(identifier_token.lexeme)
        
        return tokens
    
    def _process_segment(self, segment: str, line_num: int, column: int) -> Token:
        """澶勭悊鍒嗚瘝娈?""
        # 妫€鏌ユ槸鍚︿负鍏抽敭璇?        token_type = self._get_keyword_type(segment)
        if token_type:
            return Token(token_type, segment, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负鐧惧濮撳彉閲?        if self._is_bai_jia_xing(segment):
            return Token(TokenType.BAIJIAXING, segment, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负鍔ㄨ瘝
        arity = get_verb_arity(segment)
        if arity != 0:
            # 鏍规嵁鍏冩暟纭畾鍔ㄨ瘝绫诲瀷
            if arity == -1:
                token_type = TokenType.VERB_VAR
            elif arity == 0:
                token_type = TokenType.VERB_0
            elif arity == 1:
                token_type = TokenType.VERB_1
            elif arity == 2:
                token_type = TokenType.VERB_2
            elif arity == 3:
                token_type = TokenType.VERB_3
            else:
                token_type = TokenType.VERB_VAR
            
            return Token(token_type, segment, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负甯冨皵瀛楅潰閲?        if segment in ('鐪?, '鍋?, 'true', 'false', 'True', 'False'):
            value = segment in ('鐪?, 'true', 'True')
            return Token(TokenType.BOOLEAN, value, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负绌哄€?        if segment == '绌?:
            return Token(TokenType.NULL, None, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负鏁板瓧
        if segment.isdigit() or (segment.replace('.', '', 1).isdigit() and segment.count('.') == 1):
            try:
                if '.' in segment:
                    value = float(segment)
                else:
                    value = int(segment)
                return Token(TokenType.NUMBER, value, line_num, column, segment)
            except ValueError:
                pass
        
        # 妫€鏌ユ槸鍚︿负涓枃鏁板瓧
        if all(c in self.chinese_numbers for c in segment):
            value = self._chinese_to_arabic(segment)
            return Token(TokenType.CHINESE_NUMBER, value, line_num, column, segment)
        
        # 鏅€氭爣璇嗙
        return Token(TokenType.IDENTIFIER, segment, line_num, column, segment)
    
    def _parse_string_literal(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽瀛楃涓插瓧闈㈤噺"""
        quote_char = line[start]
        position = start + 1
        value = ''
        
        while position < len(line):
            char = line[position]
            
            if char == quote_char:
                # 缁撴潫寮曞彿
                position += 1
                break
            elif char == '\\' and position + 1 < len(line):
                # 杞箟瀛楃
                next_char = line[position + 1]
                if next_char in ('n', 't', '\\', '"', "'"):
                    value += self._escape_char(next_char)
                    position += 2
                else:
                    value += char
                    position += 1
            else:
                value += char
                position += 1
        
        lexeme = line[start:position]
        return Token(TokenType.STRING, value, line_num, column, lexeme)
    
    def _escape_char(self, char: str) -> str:
        """杞箟瀛楃"""
        escape_map = {
            'n': '\n',
            't': '\t',
            '\\': '\\',
            '"': '"',
            "'": "'",
        }
        return escape_map.get(char, char)
    
    def _parse_number(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽鏁板瓧瀛楅潰閲?""
        position = start
        
        # 瑙ｆ瀽鏁存暟閮ㄥ垎
        while position < len(line) and line[position].isdigit():
            position += 1
        
        # 瑙ｆ瀽灏忔暟閮ㄥ垎
        if position < len(line) and line[position] == '.':
            position += 1
            while position < len(line) and line[position].isdigit():
                position += 1
        
        # 瑙ｆ瀽绉戝璁℃暟娉?        if position < len(line) and line[position].lower() == 'e':
            position += 1
            if position < len(line) and line[position] in ('+', '-'):
                position += 1
            while position < len(line) and line[position].isdigit():
                position += 1
        
        lexeme = line[start:position]
        
        # 灏濊瘯杞崲涓烘暟瀛?        try:
            if '.' in lexeme or 'e' in lexeme.lower():
                value = float(lexeme)
            else:
                value = int(lexeme)
        except ValueError:
            value = lexeme  # 淇濇寔鍘熸牱
        
        return Token(TokenType.NUMBER, value, line_num, column, lexeme)
    
    def _parse_chinese_number(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽涓枃鏁板瓧"""
        position = start
        lexeme = ''
        
        while position < len(line) and line[position] in self.chinese_numbers:
            lexeme += line[position]
            position += 1
        
        # 杞崲涓洪樋鎷変集鏁板瓧
        value = self._chinese_to_arabic(lexeme)
        
        return Token(TokenType.CHINESE_NUMBER, value, line_num, column, lexeme)
    
    def _chinese_to_arabic(self, chinese_num: str) -> int:
        """灏嗕腑鏂囨暟瀛楄浆鎹负闃挎媺浼暟瀛?""
        if not chinese_num:
            return 0
        
        # 绠€鍗曞疄鐜帮紝鍙鐞嗗熀鏈暟瀛?        total = 0
        current = 0
        
        for char in chinese_num:
            num = self.chinese_numbers.get(char, 0)
            
            if num < 10:
                current = num
            elif num >= 10:
                if current == 0:
                    current = 1
                total += current * num
                current = 0
        
        total += current
        return total
    
    def _parse_identifier(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽鏍囪瘑绗?""
        position = start
        
        # 鏀堕泦鏍囪瘑绗﹀瓧绗?        while position < len(line) and self._is_identifier_char(line[position]):
            position += 1
        
        lexeme = line[start:position]
        
        # 妫€鏌ユ槸鍚︿负鍏抽敭璇?        token_type = self._get_keyword_type(lexeme)
        if token_type:
            return Token(token_type, lexeme, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负鐧惧濮撳彉閲?        if self._is_bai_jia_xing(lexeme):
            return Token(TokenType.BAIJIAXING, lexeme, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负鍔ㄨ瘝
        arity = get_verb_arity(lexeme)
        if arity != 0:
            # 鏍规嵁鍏冩暟纭畾鍔ㄨ瘝绫诲瀷
            if arity == -1:
                token_type = TokenType.VERB_VAR
            elif arity == 0:
                token_type = TokenType.VERB_0
            elif arity == 1:
                token_type = TokenType.VERB_1
            elif arity == 2:
                token_type = TokenType.VERB_2
            elif arity == 3:
                token_type = TokenType.VERB_3
            else:
                token_type = TokenType.VERB_VAR
            
            return Token(token_type, lexeme, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负甯冨皵瀛楅潰閲?        if lexeme in ('鐪?, '鍋?, 'true', 'false', 'True', 'False'):
            value = lexeme in ('鐪?, 'true', 'True')
            return Token(TokenType.BOOLEAN, value, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负绌哄€?        if lexeme == '绌?:
            return Token(TokenType.NULL, None, line_num, column, lexeme)
        
        # 灏濊瘯涓枃鍒嗚瘝
        if len(lexeme) > 1 and any('\u4e00' <= c <= '\u9fff' for c in lexeme):
            # 浣跨敤jieba杩涜涓枃鍒嗚瘝
            segments = self._segment(lexeme)
            if len(segments) > 1:
                # 濡傛灉鏄涓瘝锛岃繑鍥炵涓€涓瘝浣滀负鏍囪瘑绗?                first_segment = segments[0]
                # 閫掑綊澶勭悊绗竴涓瘝
                return self._parse_identifier(first_segment, 0, line_num, column)
        
        # 鏅€氭爣璇嗙
        return Token(TokenType.IDENTIFIER, lexeme, line_num, column, lexeme)
    
    def _is_identifier_char(self, char: str) -> bool:
        """妫€鏌ュ瓧绗︽槸鍚︿负鏍囪瘑绗﹀瓧绗?""
        # 涓枃瀛楃銆佽嫳鏂囧瓧姣嶃€佹暟瀛椼€佷笅鍒掔嚎
        return ('\u4e00' <= char <= '\u9fff' or
                'a' <= char <= 'z' or
                'A' <= char <= 'Z' or
                char.isdigit() or
                char == '_')
    
    def _get_keyword_type(self, lexeme: str) -> Optional[TokenType]:
        """鑾峰彇鍏抽敭璇嶇被鍨?""
        # 妫€鏌ョ姸鎬佸叧閿瘝锛堝瀛楋級
        for keyword, token_type in self.state_keywords.items():
            if lexeme.startswith(keyword):
                return token_type
        
        # 妫€鏌ユ劅鐭ュ叧閿瘝锛堝瀛楋級
        for keyword, token_type in self.perception_keywords.items():
            if lexeme.startswith(keyword):
                return token_type
        
        # 妫€鏌ユ椂闂村叧閿瘝锛堝瀛楋級
        for keyword, token_type in self.time_keywords.items():
            if lexeme.startswith(keyword):
                return token_type
        
        # 妫€鏌ユ櫘閫氬叧閿瘝
        return self.keywords.get(lexeme)
    
    def _is_bai_jia_xing(self, lexeme: str) -> bool:
        """妫€鏌ユ槸鍚︿负鐧惧濮撳彉閲?""
        if not lexeme:
            return False
        
        # 鑾峰彇濮撴皬锛堢涓€涓瓧绗︼級
        surname = lexeme[0]
        
        # 妫€鏌ユ槸鍚︿负鍐茬獊濮撴皬
        if surname in self.conflict_surnames:
            return False
        
        # 妫€鏌ユ槸鍚︿负鐧惧濮?        return surname in self.bai_jia_xing
    
    def print_tokens(self, tokens: List[Token]) -> None:
        """鎵撳嵃璇嶆硶鍗曞厓鍒楄〃"""
        print("璇嶆硶鍒嗘瀽缁撴灉:")
        print("=" * 80)
        print(f"{'琛?:<4} {'鍒?:<4} {'绫诲瀷':<20} {'鍊?:<20} {'璇嶇礌':<20}")
        print("-" * 80)
        
        for token in tokens:
            value_str = str(token.value)
            if len(value_str) > 18:
                value_str = value_str[:15] + "..."
            
            lexeme_str = token.lexeme
            if len(lexeme_str) > 18:
                lexeme_str = lexeme_str[:15] + "..."
            
            print(f"{token.line:<4} {token.column:<4} {token.type.value:<20} {value_str:<20} {lexeme_str:<20}")
        
        print("=" * 80)


# 娴嬭瘯鍑芥暟
def test_lexer():
    """娴嬭瘯璇嶆硶鍒嗘瀽鍣?""
    print("璇嶆硶鍒嗘瀽鍣ㄦ祴璇?)
    print("=" * 50)
    
    lexer = YanLuLexer()
    
    # 娴嬭瘯鐢ㄤ緥
    test_cases = [
        (
            "瀹氭俯搴︽槸25銆?,
            "鍙橀噺瀹氫箟"
        ),
        (
            "濡傛灉娓╁害澶?0灏卞紑鍚鎵囥€?,
            "鏉′欢璇彞"
        ),
        (
            "瀵逛簬i鍦?鍒?0锛氬嵃i銆?,
            "寰幆璇彞"
        ),
        (
            "娓╁害鍙樹负30搴︺€?,
            "鐘舵€佽浆鎹?
        ),
        (
            "寮犱笁銆佹潕鍥涳紝璁＄畻鎶樻墸銆?,
            "鎰忓悎寮忓嚱鏁拌皟鐢?
        ),
        (
            "'浣犲ソ锛屼笘鐣?",
            "瀛楃涓插瓧闈㈤噺"
        ),
        (
            "鐪熶笖鍋?,
            "甯冨皵杩愮畻"
        ),
        (
            "瀹歺绛変簬鍗佸姞浜斻€?,
            "涓枃鏁板瓧"
        ),
    ]
    
    for source_code, description in test_cases:
        print(f"\n娴嬭瘯: {description}")
        print(f"婧愪唬鐮? {source_code}")
        
        try:
            tokens = lexer.tokenize(source_code)
            lexer.print_tokens(tokens)
        except Exception as e:
            print(f"閿欒: {e}")
    
    print("=" * 50)
    print("娴嬭瘯瀹屾垚")


if __name__ == "__main__":
    test_lexer())
    
    def _init_segmenter(self):
        """鍒濆鍖栧垎璇嶅櫒"""
        if self.segmenter_type == "thulac":
            try:
                import thulac
                # 浣跨敤seg_only=True鍙繘琛屽垎璇嶏紝涓嶈繘琛岃瘝鎬ф爣娉?                self.segmenter = thulac.thulac(seg_only=True, model_path=None)
                print(f"浣跨敤THULAC鍒嗚瘝鍣?(seg_only妯″紡)")
            except ImportError:
                print("璀﹀憡: 鏈畨瑁匱HULAC锛屽洖閫€鍒癹ieba鍒嗚瘝鍣?)
                print("瀹夎鍛戒护: pip install thulac")
                self.segmenter_type = "jieba"
                self.segmenter = jieba
        else:
            # 榛樿浣跨敤jieba
            self.segmenter = jieba
            print(f"浣跨敤jieba鍒嗚瘝鍣?)
    
    def _segment(self, text: str) -> List[str]:
        """
        鍒嗚瘝鏂规硶
        
        Args:
            text: 寰呭垎璇嶇殑鏂囨湰
            
        Returns:
            鍒嗚瘝缁撴灉鍒楄〃
        """
        if self.segmenter_type == "thulac":
            # THULAC鍒嗚瘝
            result = self.segmenter.cut(text, text=True)
            return result.split()
        else:
            # jieba鍒嗚瘝
            return list(self.segmenter.lcut(text))
        
    def tokenize(self, source_code: str) -> List[Token]:
        """
        灏嗘簮浠ｇ爜杞崲涓鸿瘝娉曞崟鍏冨垪琛?        
        Args:
            source_code: 婧愪唬鐮佸瓧绗︿覆
            
        Returns:
            璇嶆硶鍗曞厓鍒楄〃
        """
        tokens = []
        lines = source_code.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            line_tokens = self._tokenize_line(line, line_num)
            tokens.extend(line_tokens)
            
            # 娣诲姞鎹㈣绗︼紙闄ら潪鏄渶鍚庝竴琛岋級
            if line_num < len(lines):
                tokens.append(Token(TokenType.NEWLINE, '\n', line_num, len(line) + 1, '\n'))
        
        # 娣诲姞鏂囦欢缁撴潫鏍囪
        tokens.append(Token(TokenType.EOF, '', len(lines) + 1, 1, ''))
        
        return tokens
    
    def _tokenize_line(self, line: str, line_num: int) -> List[Token]:
        """灏嗕竴琛屼唬鐮佽浆鎹负璇嶆硶鍗曞厓鍒楄〃"""
        tokens = []
        position = 0
        column = 1
        
        # 浣跨敤鍒嗚瘝鍣ㄨ繘琛屼腑鏂囧垎璇?        segments = self._segment(line)
        segment_index = 0
        
        while position < len(line):
            # 璺宠繃绌虹櫧瀛楃
            if line[position].isspace():
                if line[position] == '\n':
                    tokens.append(Token(TokenType.NEWLINE, '\n', line_num, column, '\n'))
                position += 1
                column += 1
                continue
            
            # 澶勭悊娉ㄩ噴
            if line[position] == '#':
                # 鍗曡娉ㄩ噴锛岃烦杩囨暣琛?                comment = line[position:]
                tokens.append(Token(TokenType.COMMENT, comment, line_num, column, comment))
                break
            
            # 澶勭悊澶氳瑷€浠ｇ爜鍧?            if line[position:position+2] == '{{':
                tokens.append(Token(TokenType.CODE_BLOCK_START, '{{', line_num, column, '{{'))
                position += 2
                column += 2
                continue
            
            if line[position:position+2] == '}}':
                tokens.append(Token(TokenType.CODE_BLOCK_END, '}}', line_num, column, '}}'))
                position += 2
                column += 2
                continue
            
            # 澶勭悊涓枃鏍囩偣绗﹀彿
            if line[position] in self.chinese_punctuation:
                char = line[position]
                token_type = self.chinese_punctuation[char]
                
                # 澶勭悊鎴愬鏍囩偣绗﹀彿
                if char in ('銆?, '銆?):
                    # 鏌ユ壘鍖归厤鐨勭粨鏉熺鍙?                    end_pos = line.find('銆? if char == '銆? else '銆?, position + 1)
                    if end_pos != -1:
                        value = line[position:end_pos + 1]
                        tokens.append(Token(token_type, value, line_num, column, value))
                        position = end_pos + 1
                        column += len(value)
                        continue
                
                tokens.append(Token(token_type, char, line_num, column, char))
                position += 1
                column += 1
                continue
            
            # 澶勭悊鐪佺暐鍙?            if line[position:position+2] == '鈥︹€?:
                tokens.append(Token(TokenType.ELLIPSIS, '鈥︹€?, line_num, column, '鈥︹€?))
                position += 2
                column += 2
                continue
            
            # 澶勭悊鐮存姌鍙?            if line[position:position+2] == '鈥斺€?:
                tokens.append(Token(TokenType.DASH, '鈥斺€?, line_num, column, '鈥斺€?))
                position += 2
                column += 2
                continue
            
            # 澶勭悊鍦嗗湀鍙?            if line[position] in '鈶犫憽鈶⑩懀鈶も懃鈶︹懅鈶ㄢ懇':
                tokens.append(Token(TokenType.CIRCLED_NUMBERS, line[position], line_num, column, line[position]))
                position += 1
                column += 1
                continue
            
            # 澶勭悊杩愮畻绗?            if line[position] in self.operators:
                # 妫€鏌ュ弻瀛楃杩愮畻绗?                if position + 1 < len(line):
                    two_char = line[position:position+2]
                    if two_char in ('鈮?, '鈮?, '鈮?):
                        tokens.append(Token(self.operators[two_char], two_char, line_num, column, two_char))
                        position += 2
                        column += 2
                        continue
                
                tokens.append(Token(self.operators[line[position]], line[position], line_num, column, line[position]))
                position += 1
                column += 1
                continue
            
            # 澶勭悊鍒嗙粍绗﹀彿
            if line[position] in self.grouping_symbols:
                tokens.append(Token(self.grouping_symbols[line[position]], line[position], line_num, column, line[position]))
                position += 1
                column += 1
                continue
            
            # 澶勭悊瀛楃涓插瓧闈㈤噺
            if line[position] in ('"', "'"):
                string_token = self._parse_string_literal(line, position, line_num, column)
                tokens.append(string_token)
                position += len(string_token.lexeme)
                column += len(string_token.lexeme)
                continue
            
            # 澶勭悊鏁板瓧瀛楅潰閲?            if line[position].isdigit() or (line[position] == '.' and position + 1 < len(line) and line[position + 1].isdigit()):
                number_token = self._parse_number(line, position, line_num, column)
                tokens.append(number_token)
                position += len(number_token.lexeme)
                column += len(number_token.lexeme)
                continue
            
            # 澶勭悊涓枃鏁板瓧
            if line[position] in self.chinese_numbers:
                chinese_number_token = self._parse_chinese_number(line, position, line_num, column)
                tokens.append(chinese_number_token)
                position += len(chinese_number_token.lexeme)
                column += len(chinese_number_token.lexeme)
                continue
            
            # 澶勭悊褰撳墠鍒嗚瘝娈?            if segment_index < len(segments):
                segment = segments[segment_index].strip()
                if segment:  # 璺宠繃绌哄垎璇?                    # 澶勭悊鍒嗚瘝娈?                    token = self._process_segment(segment, line_num, column)
                    tokens.append(token)
                    position += len(segment)
                    column += len(segment)
                segment_index += 1
            else:
                # 濡傛灉娌℃湁鏇村鍒嗚瘝锛屽鐞嗗墿浣欏瓧绗?                identifier_token = self._parse_identifier(line, position, line_num, column)
                tokens.append(identifier_token)
                position += len(identifier_token.lexeme)
                column += len(identifier_token.lexeme)
        
        return tokens
    
    def _process_segment(self, segment: str, line_num: int, column: int) -> Token:
        """澶勭悊鍒嗚瘝娈?""
        # 妫€鏌ユ槸鍚︿负鍏抽敭璇?        token_type = self._get_keyword_type(segment)
        if token_type:
            return Token(token_type, segment, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负鐧惧濮撳彉閲?        if self._is_bai_jia_xing(segment):
            return Token(TokenType.BAIJIAXING, segment, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负鍔ㄨ瘝
        arity = get_verb_arity(segment)
        if arity != 0:
            # 鏍规嵁鍏冩暟纭畾鍔ㄨ瘝绫诲瀷
            if arity == -1:
                token_type = TokenType.VERB_VAR
            elif arity == 0:
                token_type = TokenType.VERB_0
            elif arity == 1:
                token_type = TokenType.VERB_1
            elif arity == 2:
                token_type = TokenType.VERB_2
            elif arity == 3:
                token_type = TokenType.VERB_3
            else:
                token_type = TokenType.VERB_VAR
            
            return Token(token_type, segment, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负甯冨皵瀛楅潰閲?        if segment in ('鐪?, '鍋?, 'true', 'false', 'True', 'False'):
            value = segment in ('鐪?, 'true', 'True')
            return Token(TokenType.BOOLEAN, value, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负绌哄€?        if segment == '绌?:
            return Token(TokenType.NULL, None, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负鏁板瓧
        if segment.isdigit() or (segment.replace('.', '', 1).isdigit() and segment.count('.') == 1):
            try:
                if '.' in segment:
                    value = float(segment)
                else:
                    value = int(segment)
                return Token(TokenType.NUMBER, value, line_num, column, segment)
            except ValueError:
                pass
        
        # 妫€鏌ユ槸鍚︿负涓枃鏁板瓧
        if all(c in self.chinese_numbers for c in segment):
            value = self._chinese_to_arabic(segment)
            return Token(TokenType.CHINESE_NUMBER, value, line_num, column, segment)
        
        # 鏅€氭爣璇嗙
        return Token(TokenType.IDENTIFIER, segment, line_num, column, segment)
    
    def _parse_string_literal(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽瀛楃涓插瓧闈㈤噺"""
        quote_char = line[start]
        position = start + 1
        value = ''
        
        while position < len(line):
            char = line[position]
            
            if char == quote_char:
                # 缁撴潫寮曞彿
                position += 1
                break
            elif char == '\\' and position + 1 < len(line):
                # 杞箟瀛楃
                next_char = line[position + 1]
                if next_char in ('n', 't', '\\', '"', "'"):
                    value += self._escape_char(next_char)
                    position += 2
                else:
                    value += char
                    position += 1
            else:
                value += char
                position += 1
        
        lexeme = line[start:position]
        return Token(TokenType.STRING, value, line_num, column, lexeme)
    
    def _escape_char(self, char: str) -> str:
        """杞箟瀛楃"""
        escape_map = {
            'n': '\n',
            't': '\t',
            '\\': '\\',
            '"': '"',
            "'": "'",
        }
        return escape_map.get(char, char)
    
    def _parse_number(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽鏁板瓧瀛楅潰閲?""
        position = start
        
        # 瑙ｆ瀽鏁存暟閮ㄥ垎
        while position < len(line) and line[position].isdigit():
            position += 1
        
        # 瑙ｆ瀽灏忔暟閮ㄥ垎
        if position < len(line) and line[position] == '.':
            position += 1
            while position < len(line) and line[position].isdigit():
                position += 1
        
        # 瑙ｆ瀽绉戝璁℃暟娉?        if position < len(line) and line[position].lower() == 'e':
            position += 1
            if position < len(line) and line[position] in ('+', '-'):
                position += 1
            while position < len(line) and line[position].isdigit():
                position += 1
        
        lexeme = line[start:position]
        
        # 灏濊瘯杞崲涓烘暟瀛?        try:
            if '.' in lexeme or 'e' in lexeme.lower():
                value = float(lexeme)
            else:
                value = int(lexeme)
        except ValueError:
            value = lexeme  # 淇濇寔鍘熸牱
        
        return Token(TokenType.NUMBER, value, line_num, column, lexeme)
    
    def _parse_chinese_number(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽涓枃鏁板瓧"""
        position = start
        lexeme = ''
        
        while position < len(line) and line[position] in self.chinese_numbers:
            lexeme += line[position]
            position += 1
        
        # 杞崲涓洪樋鎷変集鏁板瓧
        value = self._chinese_to_arabic(lexeme)
        
        return Token(TokenType.CHINESE_NUMBER, value, line_num, column, lexeme)
    
    def _chinese_to_arabic(self, chinese_num: str) -> int:
        """灏嗕腑鏂囨暟瀛楄浆鎹负闃挎媺浼暟瀛?""
        if not chinese_num:
            return 0
        
        # 绠€鍗曞疄鐜帮紝鍙鐞嗗熀鏈暟瀛?        total = 0
        current = 0
        
        for char in chinese_num:
            num = self.chinese_numbers.get(char, 0)
            
            if num < 10:
                current = num
            elif num >= 10:
                if current == 0:
                    current = 1
                total += current * num
                current = 0
        
        total += current
        return total
    
    def _parse_identifier(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽鏍囪瘑绗?""
        position = start
        
        # 鏀堕泦鏍囪瘑绗﹀瓧绗?        while position < len(line) and self._is_identifier_char(line[position]):
            position += 1
        
        lexeme = line[start:position]
        
        # 妫€鏌ユ槸鍚︿负鍏抽敭璇?        token_type = self._get_keyword_type(lexeme)
        if token_type:
            return Token(token_type, lexeme, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负鐧惧濮撳彉閲?        if self._is_bai_jia_xing(lexeme):
            return Token(TokenType.BAIJIAXING, lexeme, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负鍔ㄨ瘝
        arity = get_verb_arity(lexeme)
        if arity != 0:
            # 鏍规嵁鍏冩暟纭畾鍔ㄨ瘝绫诲瀷
            if arity == -1:
                token_type = TokenType.VERB_VAR
            elif arity == 0:
                token_type = TokenType.VERB_0
            elif arity == 1:
                token_type = TokenType.VERB_1
            elif arity == 2:
                token_type = TokenType.VERB_2
            elif arity == 3:
                token_type = TokenType.VERB_3
            else:
                token_type = TokenType.VERB_VAR
            
            return Token(token_type, lexeme, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负甯冨皵瀛楅潰閲?        if lexeme in ('鐪?, '鍋?, 'true', 'false', 'True', 'False'):
            value = lexeme in ('鐪?, 'true', 'True')
            return Token(TokenType.BOOLEAN, value, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负绌哄€?        if lexeme == '绌?:
            return Token(TokenType.NULL, None, line_num, column, lexeme)
        
        # 灏濊瘯涓枃鍒嗚瘝
        if len(lexeme) > 1 and any('\u4e00' <= c <= '\u9fff' for c in lexeme):
            # 浣跨敤jieba杩涜涓枃鍒嗚瘝
            segments = self._segment(lexeme)
            if len(segments) > 1:
                # 濡傛灉鏄涓瘝锛岃繑鍥炵涓€涓瘝浣滀负鏍囪瘑绗?                first_segment = segments[0]
                # 閫掑綊澶勭悊绗竴涓瘝
                return self._parse_identifier(first_segment, 0, line_num, column)
        
        # 鏅€氭爣璇嗙
        return Token(TokenType.IDENTIFIER, lexeme, line_num, column, lexeme)
    
    def _is_identifier_char(self, char: str) -> bool:
        """妫€鏌ュ瓧绗︽槸鍚︿负鏍囪瘑绗﹀瓧绗?""
        # 涓枃瀛楃銆佽嫳鏂囧瓧姣嶃€佹暟瀛椼€佷笅鍒掔嚎
        return ('\u4e00' <= char <= '\u9fff' or
                'a' <= char <= 'z' or
                'A' <= char <= 'Z' or
                char.isdigit() or
                char == '_')
    
    def _get_keyword_type(self, lexeme: str) -> Optional[TokenType]:
        """鑾峰彇鍏抽敭璇嶇被鍨?""
        # 妫€鏌ョ姸鎬佸叧閿瘝锛堝瀛楋級
        for keyword, token_type in self.state_keywords.items():
            if lexeme.startswith(keyword):
                return token_type
        
        # 妫€鏌ユ劅鐭ュ叧閿瘝锛堝瀛楋級
        for keyword, token_type in self.perception_keywords.items():
            if lexeme.startswith(keyword):
                return token_type
        
        # 妫€鏌ユ椂闂村叧閿瘝锛堝瀛楋級
        for keyword, token_type in self.time_keywords.items():
            if lexeme.startswith(keyword):
                return token_type
        
        # 妫€鏌ユ櫘閫氬叧閿瘝
        return self.keywords.get(lexeme)
    
    def _is_bai_jia_xing(self, lexeme: str) -> bool:
        """妫€鏌ユ槸鍚︿负鐧惧濮撳彉閲?""
        if not lexeme:
            return False
        
        # 鑾峰彇濮撴皬锛堢涓€涓瓧绗︼級
        surname = lexeme[0]
        
        # 妫€鏌ユ槸鍚︿负鍐茬獊濮撴皬
        if surname in self.conflict_surnames:
            return False
        
        # 妫€鏌ユ槸鍚︿负鐧惧濮?        return surname in self.bai_jia_xing
    
    def print_tokens(self, tokens: List[Token]) -> None:
        """鎵撳嵃璇嶆硶鍗曞厓鍒楄〃"""
        print("璇嶆硶鍒嗘瀽缁撴灉:")
        print("=" * 80)
        print(f"{'琛?:<4} {'鍒?:<4} {'绫诲瀷':<20} {'鍊?:<20} {'璇嶇礌':<20}")
        print("-" * 80)
        
        for token in tokens:
            value_str = str(token.value)
            if len(value_str) > 18:
                value_str = value_str[:15] + "..."
            
            lexeme_str = token.lexeme
            if len(lexeme_str) > 18:
                lexeme_str = lexeme_str[:15] + "..."
            
            print(f"{token.line:<4} {token.column:<4} {token.type.value:<20} {value_str:<20} {lexeme_str:<20}")
        
        print("=" * 80)


# 娴嬭瘯鍑芥暟
def test_lexer():
    """娴嬭瘯璇嶆硶鍒嗘瀽鍣?""
    print("璇嶆硶鍒嗘瀽鍣ㄦ祴璇?)
    print("=" * 50)
    
    lexer = YanLuLexer()
    
    # 娴嬭瘯鐢ㄤ緥
    test_cases = [
        (
            "瀹氭俯搴︽槸25銆?,
            "鍙橀噺瀹氫箟"
        ),
        (
            "濡傛灉娓╁害澶?0灏卞紑鍚鎵囥€?,
            "鏉′欢璇彞"
        ),
        (
            "瀵逛簬i鍦?鍒?0锛氬嵃i銆?,
            "寰幆璇彞"
        ),
        (
            "娓╁害鍙樹负30搴︺€?,
            "鐘舵€佽浆鎹?
        ),
        (
            "寮犱笁銆佹潕鍥涳紝璁＄畻鎶樻墸銆?,
            "鎰忓悎寮忓嚱鏁拌皟鐢?
        ),
        (
            "'浣犲ソ锛屼笘鐣?",
            "瀛楃涓插瓧闈㈤噺"
        ),
        (
            "鐪熶笖鍋?,
            "甯冨皵杩愮畻"
        ),
        (
            "瀹歺绛変簬鍗佸姞浜斻€?,
            "涓枃鏁板瓧"
        ),
    ]
    
    for source_code, description in test_cases:
        print(f"\n娴嬭瘯: {description}")
        print(f"婧愪唬鐮? {source_code}")
        
        try:
            tokens = lexer.tokenize(source_code)
            lexer.print_tokens(tokens)
        except Exception as e:
            print(f"閿欒: {e}")
    
    print("=" * 50)
    print("娴嬭瘯瀹屾垚")


if __name__ == "__main__":
    test_lexer())
        self.identifier_pattern = re.compile(r'^[\u4e00-\u9fffA-Za-z_][\u4e00-\u9fffA-Za-z0-9_]*
        """
        灏嗘簮浠ｇ爜杞崲涓鸿瘝娉曞崟鍏冨垪琛?        
        Args:
            source_code: 婧愪唬鐮佸瓧绗︿覆
            
        Returns:
            璇嶆硶鍗曞厓鍒楄〃
        """
        tokens = []
        lines = source_code.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            line_tokens = self._tokenize_line(line, line_num)
            tokens.extend(line_tokens)
            
            # 娣诲姞鎹㈣绗︼紙闄ら潪鏄渶鍚庝竴琛岋級
            if line_num < len(lines):
                tokens.append(Token(TokenType.NEWLINE, '\n', line_num, len(line) + 1, '\n'))
        
        # 娣诲姞鏂囦欢缁撴潫鏍囪
        tokens.append(Token(TokenType.EOF, '', len(lines) + 1, 1, ''))
        
        return tokens
    
    def _tokenize_line(self, line: str, line_num: int) -> List[Token]:
        """灏嗕竴琛屼唬鐮佽浆鎹负璇嶆硶鍗曞厓鍒楄〃"""
        tokens = []
        position = 0
        column = 1
        
        # 浣跨敤鍒嗚瘝鍣ㄨ繘琛屼腑鏂囧垎璇?        segments = self._segment(line)
        segment_index = 0
        
        while position < len(line):
            # 璺宠繃绌虹櫧瀛楃
            if line[position].isspace():
                if line[position] == '\n':
                    tokens.append(Token(TokenType.NEWLINE, '\n', line_num, column, '\n'))
                position += 1
                column += 1
                continue
            
            # 澶勭悊娉ㄩ噴
            if line[position] == '#':
                # 鍗曡娉ㄩ噴锛岃烦杩囨暣琛?                comment = line[position:]
                tokens.append(Token(TokenType.COMMENT, comment, line_num, column, comment))
                break
            
            # 澶勭悊澶氳瑷€浠ｇ爜鍧?            if line[position:position+2] == '{{':
                tokens.append(Token(TokenType.CODE_BLOCK_START, '{{', line_num, column, '{{'))
                position += 2
                column += 2
                continue
            
            if line[position:position+2] == '}}':
                tokens.append(Token(TokenType.CODE_BLOCK_END, '}}', line_num, column, '}}'))
                position += 2
                column += 2
                continue
            
            # 澶勭悊涓枃鏍囩偣绗﹀彿
            if line[position] in self.chinese_punctuation:
                char = line[position]
                token_type = self.chinese_punctuation[char]
                
                # 澶勭悊鎴愬鏍囩偣绗﹀彿
                if char in ('銆?, '銆?):
                    # 鏌ユ壘鍖归厤鐨勭粨鏉熺鍙?                    end_pos = line.find('銆? if char == '銆? else '銆?, position + 1)
                    if end_pos != -1:
                        value = line[position:end_pos + 1]
                        tokens.append(Token(token_type, value, line_num, column, value))
                        position = end_pos + 1
                        column += len(value)
                        continue
                
                tokens.append(Token(token_type, char, line_num, column, char))
                position += 1
                column += 1
                continue
            
            # 澶勭悊鐪佺暐鍙?            if line[position:position+2] == '鈥︹€?:
                tokens.append(Token(TokenType.ELLIPSIS, '鈥︹€?, line_num, column, '鈥︹€?))
                position += 2
                column += 2
                continue
            
            # 澶勭悊鐮存姌鍙?            if line[position:position+2] == '鈥斺€?:
                tokens.append(Token(TokenType.DASH, '鈥斺€?, line_num, column, '鈥斺€?))
                position += 2
                column += 2
                continue
            
            # 澶勭悊鍦嗗湀鍙?            if line[position] in '鈶犫憽鈶⑩懀鈶も懃鈶︹懅鈶ㄢ懇':
                tokens.append(Token(TokenType.CIRCLED_NUMBERS, line[position], line_num, column, line[position]))
                position += 1
                column += 1
                continue
            
            # 澶勭悊杩愮畻绗?            if line[position] in self.operators:
                # 妫€鏌ュ弻瀛楃杩愮畻绗?                if position + 1 < len(line):
                    two_char = line[position:position+2]
                    if two_char in ('鈮?, '鈮?, '鈮?):
                        tokens.append(Token(self.operators[two_char], two_char, line_num, column, two_char))
                        position += 2
                        column += 2
                        continue
                
                tokens.append(Token(self.operators[line[position]], line[position], line_num, column, line[position]))
                position += 1
                column += 1
                continue
            
            # 澶勭悊鍒嗙粍绗﹀彿
            if line[position] in self.grouping_symbols:
                tokens.append(Token(self.grouping_symbols[line[position]], line[position], line_num, column, line[position]))
                position += 1
                column += 1
                continue
            
            # 澶勭悊瀛楃涓插瓧闈㈤噺
            if line[position] in ('"', "'"):
                string_token = self._parse_string_literal(line, position, line_num, column)
                tokens.append(string_token)
                position += len(string_token.lexeme)
                column += len(string_token.lexeme)
                continue
            
            # 澶勭悊鏁板瓧瀛楅潰閲?            if line[position].isdigit() or (line[position] == '.' and position + 1 < len(line) and line[position + 1].isdigit()):
                number_token = self._parse_number(line, position, line_num, column)
                tokens.append(number_token)
                position += len(number_token.lexeme)
                column += len(number_token.lexeme)
                continue
            
            # 澶勭悊涓枃鏁板瓧
            if line[position] in self.chinese_numbers:
                chinese_number_token = self._parse_chinese_number(line, position, line_num, column)
                tokens.append(chinese_number_token)
                position += len(chinese_number_token.lexeme)
                column += len(chinese_number_token.lexeme)
                continue
            
            # 澶勭悊褰撳墠鍒嗚瘝娈?            if segment_index < len(segments):
                segment = segments[segment_index].strip()
                if segment:  # 璺宠繃绌哄垎璇?                    # 澶勭悊鍒嗚瘝娈?                    token = self._process_segment(segment, line_num, column)
                    tokens.append(token)
                    position += len(segment)
                    column += len(segment)
                segment_index += 1
            else:
                # 濡傛灉娌℃湁鏇村鍒嗚瘝锛屽鐞嗗墿浣欏瓧绗?                identifier_token = self._parse_identifier(line, position, line_num, column)
                tokens.append(identifier_token)
                position += len(identifier_token.lexeme)
                column += len(identifier_token.lexeme)
        
        return tokens
    
    def _process_segment(self, segment: str, line_num: int, column: int) -> Token:
        """澶勭悊鍒嗚瘝娈?""
        # 妫€鏌ユ槸鍚︿负鍏抽敭璇?        token_type = self._get_keyword_type(segment)
        if token_type:
            return Token(token_type, segment, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负鐧惧濮撳彉閲?        if self._is_bai_jia_xing(segment):
            return Token(TokenType.BAIJIAXING, segment, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负鍔ㄨ瘝
        arity = get_verb_arity(segment)
        if arity != 0:
            # 鏍规嵁鍏冩暟纭畾鍔ㄨ瘝绫诲瀷
            if arity == -1:
                token_type = TokenType.VERB_VAR
            elif arity == 0:
                token_type = TokenType.VERB_0
            elif arity == 1:
                token_type = TokenType.VERB_1
            elif arity == 2:
                token_type = TokenType.VERB_2
            elif arity == 3:
                token_type = TokenType.VERB_3
            else:
                token_type = TokenType.VERB_VAR
            
            return Token(token_type, segment, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负甯冨皵瀛楅潰閲?        if segment in ('鐪?, '鍋?, 'true', 'false', 'True', 'False'):
            value = segment in ('鐪?, 'true', 'True')
            return Token(TokenType.BOOLEAN, value, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负绌哄€?        if segment == '绌?:
            return Token(TokenType.NULL, None, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负鏁板瓧
        if segment.isdigit() or (segment.replace('.', '', 1).isdigit() and segment.count('.') == 1):
            try:
                if '.' in segment:
                    value = float(segment)
                else:
                    value = int(segment)
                return Token(TokenType.NUMBER, value, line_num, column, segment)
            except ValueError:
                pass
        
        # 妫€鏌ユ槸鍚︿负涓枃鏁板瓧
        if all(c in self.chinese_numbers for c in segment):
            value = self._chinese_to_arabic(segment)
            return Token(TokenType.CHINESE_NUMBER, value, line_num, column, segment)
        
        # 鏅€氭爣璇嗙
        return Token(TokenType.IDENTIFIER, segment, line_num, column, segment)
    
    def _parse_string_literal(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽瀛楃涓插瓧闈㈤噺"""
        quote_char = line[start]
        position = start + 1
        value = ''
        
        while position < len(line):
            char = line[position]
            
            if char == quote_char:
                # 缁撴潫寮曞彿
                position += 1
                break
            elif char == '\\' and position + 1 < len(line):
                # 杞箟瀛楃
                next_char = line[position + 1]
                if next_char in ('n', 't', '\\', '"', "'"):
                    value += self._escape_char(next_char)
                    position += 2
                else:
                    value += char
                    position += 1
            else:
                value += char
                position += 1
        
        lexeme = line[start:position]
        return Token(TokenType.STRING, value, line_num, column, lexeme)
    
    def _escape_char(self, char: str) -> str:
        """杞箟瀛楃"""
        escape_map = {
            'n': '\n',
            't': '\t',
            '\\': '\\',
            '"': '"',
            "'": "'",
        }
        return escape_map.get(char, char)
    
    def _parse_number(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽鏁板瓧瀛楅潰閲?""
        position = start
        
        # 瑙ｆ瀽鏁存暟閮ㄥ垎
        while position < len(line) and line[position].isdigit():
            position += 1
        
        # 瑙ｆ瀽灏忔暟閮ㄥ垎
        if position < len(line) and line[position] == '.':
            position += 1
            while position < len(line) and line[position].isdigit():
                position += 1
        
        # 瑙ｆ瀽绉戝璁℃暟娉?        if position < len(line) and line[position].lower() == 'e':
            position += 1
            if position < len(line) and line[position] in ('+', '-'):
                position += 1
            while position < len(line) and line[position].isdigit():
                position += 1
        
        lexeme = line[start:position]
        
        # 灏濊瘯杞崲涓烘暟瀛?        try:
            if '.' in lexeme or 'e' in lexeme.lower():
                value = float(lexeme)
            else:
                value = int(lexeme)
        except ValueError:
            value = lexeme  # 淇濇寔鍘熸牱
        
        return Token(TokenType.NUMBER, value, line_num, column, lexeme)
    
    def _parse_chinese_number(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽涓枃鏁板瓧"""
        position = start
        lexeme = ''
        
        while position < len(line) and line[position] in self.chinese_numbers:
            lexeme += line[position]
            position += 1
        
        # 杞崲涓洪樋鎷変集鏁板瓧
        value = self._chinese_to_arabic(lexeme)
        
        return Token(TokenType.CHINESE_NUMBER, value, line_num, column, lexeme)
    
    def _chinese_to_arabic(self, chinese_num: str) -> int:
        """灏嗕腑鏂囨暟瀛楄浆鎹负闃挎媺浼暟瀛?""
        if not chinese_num:
            return 0
        
        # 绠€鍗曞疄鐜帮紝鍙鐞嗗熀鏈暟瀛?        total = 0
        current = 0
        
        for char in chinese_num:
            num = self.chinese_numbers.get(char, 0)
            
            if num < 10:
                current = num
            elif num >= 10:
                if current == 0:
                    current = 1
                total += current * num
                current = 0
        
        total += current
        return total
    
    def _parse_identifier(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽鏍囪瘑绗?""
        position = start
        
        # 鏀堕泦鏍囪瘑绗﹀瓧绗?        while position < len(line) and self._is_identifier_char(line[position]):
            position += 1
        
        lexeme = line[start:position]
        
        # 妫€鏌ユ槸鍚︿负鍏抽敭璇?        token_type = self._get_keyword_type(lexeme)
        if token_type:
            return Token(token_type, lexeme, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负鐧惧濮撳彉閲?        if self._is_bai_jia_xing(lexeme):
            return Token(TokenType.BAIJIAXING, lexeme, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负鍔ㄨ瘝
        arity = get_verb_arity(lexeme)
        if arity != 0:
            # 鏍规嵁鍏冩暟纭畾鍔ㄨ瘝绫诲瀷
            if arity == -1:
                token_type = TokenType.VERB_VAR
            elif arity == 0:
                token_type = TokenType.VERB_0
            elif arity == 1:
                token_type = TokenType.VERB_1
            elif arity == 2:
                token_type = TokenType.VERB_2
            elif arity == 3:
                token_type = TokenType.VERB_3
            else:
                token_type = TokenType.VERB_VAR
            
            return Token(token_type, lexeme, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负甯冨皵瀛楅潰閲?        if lexeme in ('鐪?, '鍋?, 'true', 'false', 'True', 'False'):
            value = lexeme in ('鐪?, 'true', 'True')
            return Token(TokenType.BOOLEAN, value, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负绌哄€?        if lexeme == '绌?:
            return Token(TokenType.NULL, None, line_num, column, lexeme)
        
        # 灏濊瘯涓枃鍒嗚瘝
        if len(lexeme) > 1 and any('\u4e00' <= c <= '\u9fff' for c in lexeme):
            # 浣跨敤jieba杩涜涓枃鍒嗚瘝
            segments = self._segment(lexeme)
            if len(segments) > 1:
                # 濡傛灉鏄涓瘝锛岃繑鍥炵涓€涓瘝浣滀负鏍囪瘑绗?                first_segment = segments[0]
                # 閫掑綊澶勭悊绗竴涓瘝
                return self._parse_identifier(first_segment, 0, line_num, column)
        
        # 鏅€氭爣璇嗙
        return Token(TokenType.IDENTIFIER, lexeme, line_num, column, lexeme)
    
    def _is_identifier_char(self, char: str) -> bool:
        """妫€鏌ュ瓧绗︽槸鍚︿负鏍囪瘑绗﹀瓧绗?""
        # 涓枃瀛楃銆佽嫳鏂囧瓧姣嶃€佹暟瀛椼€佷笅鍒掔嚎
        return ('\u4e00' <= char <= '\u9fff' or
                'a' <= char <= 'z' or
                'A' <= char <= 'Z' or
                char.isdigit() or
                char == '_')
    
    def _get_keyword_type(self, lexeme: str) -> Optional[TokenType]:
        """鑾峰彇鍏抽敭璇嶇被鍨?""
        # 妫€鏌ョ姸鎬佸叧閿瘝锛堝瀛楋級
        for keyword, token_type in self.state_keywords.items():
            if lexeme.startswith(keyword):
                return token_type
        
        # 妫€鏌ユ劅鐭ュ叧閿瘝锛堝瀛楋級
        for keyword, token_type in self.perception_keywords.items():
            if lexeme.startswith(keyword):
                return token_type
        
        # 妫€鏌ユ椂闂村叧閿瘝锛堝瀛楋級
        for keyword, token_type in self.time_keywords.items():
            if lexeme.startswith(keyword):
                return token_type
        
        # 妫€鏌ユ櫘閫氬叧閿瘝
        return self.keywords.get(lexeme)
    
    def _is_bai_jia_xing(self, lexeme: str) -> bool:
        """妫€鏌ユ槸鍚︿负鐧惧濮撳彉閲?""
        if not lexeme:
            return False
        
        # 鑾峰彇濮撴皬锛堢涓€涓瓧绗︼級
        surname = lexeme[0]
        
        # 妫€鏌ユ槸鍚︿负鍐茬獊濮撴皬
        if surname in self.conflict_surnames:
            return False
        
        # 妫€鏌ユ槸鍚︿负鐧惧濮?        return surname in self.bai_jia_xing
    
    def print_tokens(self, tokens: List[Token]) -> None:
        """鎵撳嵃璇嶆硶鍗曞厓鍒楄〃"""
        print("璇嶆硶鍒嗘瀽缁撴灉:")
        print("=" * 80)
        print(f"{'琛?:<4} {'鍒?:<4} {'绫诲瀷':<20} {'鍊?:<20} {'璇嶇礌':<20}")
        print("-" * 80)
        
        for token in tokens:
            value_str = str(token.value)
            if len(value_str) > 18:
                value_str = value_str[:15] + "..."
            
            lexeme_str = token.lexeme
            if len(lexeme_str) > 18:
                lexeme_str = lexeme_str[:15] + "..."
            
            print(f"{token.line:<4} {token.column:<4} {token.type.value:<20} {value_str:<20} {lexeme_str:<20}")
        
        print("=" * 80)


# 娴嬭瘯鍑芥暟
def test_lexer():
    """娴嬭瘯璇嶆硶鍒嗘瀽鍣?""
    print("璇嶆硶鍒嗘瀽鍣ㄦ祴璇?)
    print("=" * 50)
    
    lexer = YanLuLexer()
    
    # 娴嬭瘯鐢ㄤ緥
    test_cases = [
        (
            "瀹氭俯搴︽槸25銆?,
            "鍙橀噺瀹氫箟"
        ),
        (
            "濡傛灉娓╁害澶?0灏卞紑鍚鎵囥€?,
            "鏉′欢璇彞"
        ),
        (
            "瀵逛簬i鍦?鍒?0锛氬嵃i銆?,
            "寰幆璇彞"
        ),
        (
            "娓╁害鍙樹负30搴︺€?,
            "鐘舵€佽浆鎹?
        ),
        (
            "寮犱笁銆佹潕鍥涳紝璁＄畻鎶樻墸銆?,
            "鎰忓悎寮忓嚱鏁拌皟鐢?
        ),
        (
            "'浣犲ソ锛屼笘鐣?",
            "瀛楃涓插瓧闈㈤噺"
        ),
        (
            "鐪熶笖鍋?,
            "甯冨皵杩愮畻"
        ),
        (
            "瀹歺绛変簬鍗佸姞浜斻€?,
            "涓枃鏁板瓧"
        ),
    ]
    
    for source_code, description in test_cases:
        print(f"\n娴嬭瘯: {description}")
        print(f"婧愪唬鐮? {source_code}")
        
        try:
            tokens = lexer.tokenize(source_code)
            lexer.print_tokens(tokens)
        except Exception as e:
            print(f"閿欒: {e}")
    
    print("=" * 50)
    print("娴嬭瘯瀹屾垚")


if __name__ == "__main__":
    test_lexer())
    
    def _init_segmenter(self):
        """鍒濆鍖栧垎璇嶅櫒"""
        if self.segmenter_type == "thulac":
            try:
                import thulac
                # 浣跨敤seg_only=True鍙繘琛屽垎璇嶏紝涓嶈繘琛岃瘝鎬ф爣娉?                self.segmenter = thulac.thulac(seg_only=True, model_path=None)
                print(f"浣跨敤THULAC鍒嗚瘝鍣?(seg_only妯″紡)")
            except ImportError:
                print("璀﹀憡: 鏈畨瑁匱HULAC锛屽洖閫€鍒癹ieba鍒嗚瘝鍣?)
                print("瀹夎鍛戒护: pip install thulac")
                self.segmenter_type = "jieba"
                self.segmenter = jieba
        else:
            # 榛樿浣跨敤jieba
            self.segmenter = jieba
            print(f"浣跨敤jieba鍒嗚瘝鍣?)
    
    def _segment(self, text: str) -> List[str]:
        """
        鍒嗚瘝鏂规硶
        
        Args:
            text: 寰呭垎璇嶇殑鏂囨湰
            
        Returns:
            鍒嗚瘝缁撴灉鍒楄〃
        """
        if self.segmenter_type == "thulac":
            # THULAC鍒嗚瘝
            result = self.segmenter.cut(text, text=True)
            return result.split()
        else:
            # jieba鍒嗚瘝
            return list(self.segmenter.lcut(text))
        
    def tokenize(self, source_code: str) -> List[Token]:
        """
        灏嗘簮浠ｇ爜杞崲涓鸿瘝娉曞崟鍏冨垪琛?        
        Args:
            source_code: 婧愪唬鐮佸瓧绗︿覆
            
        Returns:
            璇嶆硶鍗曞厓鍒楄〃
        """
        tokens = []
        lines = source_code.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            line_tokens = self._tokenize_line(line, line_num)
            tokens.extend(line_tokens)
            
            # 娣诲姞鎹㈣绗︼紙闄ら潪鏄渶鍚庝竴琛岋級
            if line_num < len(lines):
                tokens.append(Token(TokenType.NEWLINE, '\n', line_num, len(line) + 1, '\n'))
        
        # 娣诲姞鏂囦欢缁撴潫鏍囪
        tokens.append(Token(TokenType.EOF, '', len(lines) + 1, 1, ''))
        
        return tokens
    
    def _tokenize_line(self, line: str, line_num: int) -> List[Token]:
        """灏嗕竴琛屼唬鐮佽浆鎹负璇嶆硶鍗曞厓鍒楄〃"""
        tokens = []
        position = 0
        column = 1
        
        # 浣跨敤鍒嗚瘝鍣ㄨ繘琛屼腑鏂囧垎璇?        segments = self._segment(line)
        segment_index = 0
        
        while position < len(line):
            # 璺宠繃绌虹櫧瀛楃
            if line[position].isspace():
                if line[position] == '\n':
                    tokens.append(Token(TokenType.NEWLINE, '\n', line_num, column, '\n'))
                position += 1
                column += 1
                continue
            
            # 澶勭悊娉ㄩ噴
            if line[position] == '#':
                # 鍗曡娉ㄩ噴锛岃烦杩囨暣琛?                comment = line[position:]
                tokens.append(Token(TokenType.COMMENT, comment, line_num, column, comment))
                break
            
            # 澶勭悊澶氳瑷€浠ｇ爜鍧?            if line[position:position+2] == '{{':
                tokens.append(Token(TokenType.CODE_BLOCK_START, '{{', line_num, column, '{{'))
                position += 2
                column += 2
                continue
            
            if line[position:position+2] == '}}':
                tokens.append(Token(TokenType.CODE_BLOCK_END, '}}', line_num, column, '}}'))
                position += 2
                column += 2
                continue
            
            # 澶勭悊涓枃鏍囩偣绗﹀彿
            if line[position] in self.chinese_punctuation:
                char = line[position]
                token_type = self.chinese_punctuation[char]
                
                # 澶勭悊鎴愬鏍囩偣绗﹀彿
                if char in ('銆?, '銆?):
                    # 鏌ユ壘鍖归厤鐨勭粨鏉熺鍙?                    end_pos = line.find('銆? if char == '銆? else '銆?, position + 1)
                    if end_pos != -1:
                        value = line[position:end_pos + 1]
                        tokens.append(Token(token_type, value, line_num, column, value))
                        position = end_pos + 1
                        column += len(value)
                        continue
                
                tokens.append(Token(token_type, char, line_num, column, char))
                position += 1
                column += 1
                continue
            
            # 澶勭悊鐪佺暐鍙?            if line[position:position+2] == '鈥︹€?:
                tokens.append(Token(TokenType.ELLIPSIS, '鈥︹€?, line_num, column, '鈥︹€?))
                position += 2
                column += 2
                continue
            
            # 澶勭悊鐮存姌鍙?            if line[position:position+2] == '鈥斺€?:
                tokens.append(Token(TokenType.DASH, '鈥斺€?, line_num, column, '鈥斺€?))
                position += 2
                column += 2
                continue
            
            # 澶勭悊鍦嗗湀鍙?            if line[position] in '鈶犫憽鈶⑩懀鈶も懃鈶︹懅鈶ㄢ懇':
                tokens.append(Token(TokenType.CIRCLED_NUMBERS, line[position], line_num, column, line[position]))
                position += 1
                column += 1
                continue
            
            # 澶勭悊杩愮畻绗?            if line[position] in self.operators:
                # 妫€鏌ュ弻瀛楃杩愮畻绗?                if position + 1 < len(line):
                    two_char = line[position:position+2]
                    if two_char in ('鈮?, '鈮?, '鈮?):
                        tokens.append(Token(self.operators[two_char], two_char, line_num, column, two_char))
                        position += 2
                        column += 2
                        continue
                
                tokens.append(Token(self.operators[line[position]], line[position], line_num, column, line[position]))
                position += 1
                column += 1
                continue
            
            # 澶勭悊鍒嗙粍绗﹀彿
            if line[position] in self.grouping_symbols:
                tokens.append(Token(self.grouping_symbols[line[position]], line[position], line_num, column, line[position]))
                position += 1
                column += 1
                continue
            
            # 澶勭悊瀛楃涓插瓧闈㈤噺
            if line[position] in ('"', "'"):
                string_token = self._parse_string_literal(line, position, line_num, column)
                tokens.append(string_token)
                position += len(string_token.lexeme)
                column += len(string_token.lexeme)
                continue
            
            # 澶勭悊鏁板瓧瀛楅潰閲?            if line[position].isdigit() or (line[position] == '.' and position + 1 < len(line) and line[position + 1].isdigit()):
                number_token = self._parse_number(line, position, line_num, column)
                tokens.append(number_token)
                position += len(number_token.lexeme)
                column += len(number_token.lexeme)
                continue
            
            # 澶勭悊涓枃鏁板瓧
            if line[position] in self.chinese_numbers:
                chinese_number_token = self._parse_chinese_number(line, position, line_num, column)
                tokens.append(chinese_number_token)
                position += len(chinese_number_token.lexeme)
                column += len(chinese_number_token.lexeme)
                continue
            
            # 澶勭悊褰撳墠鍒嗚瘝娈?            if segment_index < len(segments):
                segment = segments[segment_index].strip()
                if segment:  # 璺宠繃绌哄垎璇?                    # 澶勭悊鍒嗚瘝娈?                    token = self._process_segment(segment, line_num, column)
                    tokens.append(token)
                    position += len(segment)
                    column += len(segment)
                segment_index += 1
            else:
                # 濡傛灉娌℃湁鏇村鍒嗚瘝锛屽鐞嗗墿浣欏瓧绗?                identifier_token = self._parse_identifier(line, position, line_num, column)
                tokens.append(identifier_token)
                position += len(identifier_token.lexeme)
                column += len(identifier_token.lexeme)
        
        return tokens
    
    def _process_segment(self, segment: str, line_num: int, column: int) -> Token:
        """澶勭悊鍒嗚瘝娈?""
        # 妫€鏌ユ槸鍚︿负鍏抽敭璇?        token_type = self._get_keyword_type(segment)
        if token_type:
            return Token(token_type, segment, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负鐧惧濮撳彉閲?        if self._is_bai_jia_xing(segment):
            return Token(TokenType.BAIJIAXING, segment, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负鍔ㄨ瘝
        arity = get_verb_arity(segment)
        if arity != 0:
            # 鏍规嵁鍏冩暟纭畾鍔ㄨ瘝绫诲瀷
            if arity == -1:
                token_type = TokenType.VERB_VAR
            elif arity == 0:
                token_type = TokenType.VERB_0
            elif arity == 1:
                token_type = TokenType.VERB_1
            elif arity == 2:
                token_type = TokenType.VERB_2
            elif arity == 3:
                token_type = TokenType.VERB_3
            else:
                token_type = TokenType.VERB_VAR
            
            return Token(token_type, segment, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负甯冨皵瀛楅潰閲?        if segment in ('鐪?, '鍋?, 'true', 'false', 'True', 'False'):
            value = segment in ('鐪?, 'true', 'True')
            return Token(TokenType.BOOLEAN, value, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负绌哄€?        if segment == '绌?:
            return Token(TokenType.NULL, None, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负鏁板瓧
        if segment.isdigit() or (segment.replace('.', '', 1).isdigit() and segment.count('.') == 1):
            try:
                if '.' in segment:
                    value = float(segment)
                else:
                    value = int(segment)
                return Token(TokenType.NUMBER, value, line_num, column, segment)
            except ValueError:
                pass
        
        # 妫€鏌ユ槸鍚︿负涓枃鏁板瓧
        if all(c in self.chinese_numbers for c in segment):
            value = self._chinese_to_arabic(segment)
            return Token(TokenType.CHINESE_NUMBER, value, line_num, column, segment)
        
        # 鏅€氭爣璇嗙
        return Token(TokenType.IDENTIFIER, segment, line_num, column, segment)
    
    def _parse_string_literal(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽瀛楃涓插瓧闈㈤噺"""
        quote_char = line[start]
        position = start + 1
        value = ''
        
        while position < len(line):
            char = line[position]
            
            if char == quote_char:
                # 缁撴潫寮曞彿
                position += 1
                break
            elif char == '\\' and position + 1 < len(line):
                # 杞箟瀛楃
                next_char = line[position + 1]
                if next_char in ('n', 't', '\\', '"', "'"):
                    value += self._escape_char(next_char)
                    position += 2
                else:
                    value += char
                    position += 1
            else:
                value += char
                position += 1
        
        lexeme = line[start:position]
        return Token(TokenType.STRING, value, line_num, column, lexeme)
    
    def _escape_char(self, char: str) -> str:
        """杞箟瀛楃"""
        escape_map = {
            'n': '\n',
            't': '\t',
            '\\': '\\',
            '"': '"',
            "'": "'",
        }
        return escape_map.get(char, char)
    
    def _parse_number(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽鏁板瓧瀛楅潰閲?""
        position = start
        
        # 瑙ｆ瀽鏁存暟閮ㄥ垎
        while position < len(line) and line[position].isdigit():
            position += 1
        
        # 瑙ｆ瀽灏忔暟閮ㄥ垎
        if position < len(line) and line[position] == '.':
            position += 1
            while position < len(line) and line[position].isdigit():
                position += 1
        
        # 瑙ｆ瀽绉戝璁℃暟娉?        if position < len(line) and line[position].lower() == 'e':
            position += 1
            if position < len(line) and line[position] in ('+', '-'):
                position += 1
            while position < len(line) and line[position].isdigit():
                position += 1
        
        lexeme = line[start:position]
        
        # 灏濊瘯杞崲涓烘暟瀛?        try:
            if '.' in lexeme or 'e' in lexeme.lower():
                value = float(lexeme)
            else:
                value = int(lexeme)
        except ValueError:
            value = lexeme  # 淇濇寔鍘熸牱
        
        return Token(TokenType.NUMBER, value, line_num, column, lexeme)
    
    def _parse_chinese_number(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽涓枃鏁板瓧"""
        position = start
        lexeme = ''
        
        while position < len(line) and line[position] in self.chinese_numbers:
            lexeme += line[position]
            position += 1
        
        # 杞崲涓洪樋鎷変集鏁板瓧
        value = self._chinese_to_arabic(lexeme)
        
        return Token(TokenType.CHINESE_NUMBER, value, line_num, column, lexeme)
    
    def _chinese_to_arabic(self, chinese_num: str) -> int:
        """灏嗕腑鏂囨暟瀛楄浆鎹负闃挎媺浼暟瀛?""
        if not chinese_num:
            return 0
        
        # 绠€鍗曞疄鐜帮紝鍙鐞嗗熀鏈暟瀛?        total = 0
        current = 0
        
        for char in chinese_num:
            num = self.chinese_numbers.get(char, 0)
            
            if num < 10:
                current = num
            elif num >= 10:
                if current == 0:
                    current = 1
                total += current * num
                current = 0
        
        total += current
        return total
    
    def _parse_identifier(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽鏍囪瘑绗?""
        position = start
        
        # 鏀堕泦鏍囪瘑绗﹀瓧绗?        while position < len(line) and self._is_identifier_char(line[position]):
            position += 1
        
        lexeme = line[start:position]
        
        # 妫€鏌ユ槸鍚︿负鍏抽敭璇?        token_type = self._get_keyword_type(lexeme)
        if token_type:
            return Token(token_type, lexeme, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负鐧惧濮撳彉閲?        if self._is_bai_jia_xing(lexeme):
            return Token(TokenType.BAIJIAXING, lexeme, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负鍔ㄨ瘝
        arity = get_verb_arity(lexeme)
        if arity != 0:
            # 鏍规嵁鍏冩暟纭畾鍔ㄨ瘝绫诲瀷
            if arity == -1:
                token_type = TokenType.VERB_VAR
            elif arity == 0:
                token_type = TokenType.VERB_0
            elif arity == 1:
                token_type = TokenType.VERB_1
            elif arity == 2:
                token_type = TokenType.VERB_2
            elif arity == 3:
                token_type = TokenType.VERB_3
            else:
                token_type = TokenType.VERB_VAR
            
            return Token(token_type, lexeme, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负甯冨皵瀛楅潰閲?        if lexeme in ('鐪?, '鍋?, 'true', 'false', 'True', 'False'):
            value = lexeme in ('鐪?, 'true', 'True')
            return Token(TokenType.BOOLEAN, value, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负绌哄€?        if lexeme == '绌?:
            return Token(TokenType.NULL, None, line_num, column, lexeme)
        
        # 灏濊瘯涓枃鍒嗚瘝
        if len(lexeme) > 1 and any('\u4e00' <= c <= '\u9fff' for c in lexeme):
            # 浣跨敤jieba杩涜涓枃鍒嗚瘝
            segments = self._segment(lexeme)
            if len(segments) > 1:
                # 濡傛灉鏄涓瘝锛岃繑鍥炵涓€涓瘝浣滀负鏍囪瘑绗?                first_segment = segments[0]
                # 閫掑綊澶勭悊绗竴涓瘝
                return self._parse_identifier(first_segment, 0, line_num, column)
        
        # 鏅€氭爣璇嗙
        return Token(TokenType.IDENTIFIER, lexeme, line_num, column, lexeme)
    
    def _is_identifier_char(self, char: str) -> bool:
        """妫€鏌ュ瓧绗︽槸鍚︿负鏍囪瘑绗﹀瓧绗?""
        # 涓枃瀛楃銆佽嫳鏂囧瓧姣嶃€佹暟瀛椼€佷笅鍒掔嚎
        return ('\u4e00' <= char <= '\u9fff' or
                'a' <= char <= 'z' or
                'A' <= char <= 'Z' or
                char.isdigit() or
                char == '_')
    
    def _get_keyword_type(self, lexeme: str) -> Optional[TokenType]:
        """鑾峰彇鍏抽敭璇嶇被鍨?""
        # 妫€鏌ョ姸鎬佸叧閿瘝锛堝瀛楋級
        for keyword, token_type in self.state_keywords.items():
            if lexeme.startswith(keyword):
                return token_type
        
        # 妫€鏌ユ劅鐭ュ叧閿瘝锛堝瀛楋級
        for keyword, token_type in self.perception_keywords.items():
            if lexeme.startswith(keyword):
                return token_type
        
        # 妫€鏌ユ椂闂村叧閿瘝锛堝瀛楋級
        for keyword, token_type in self.time_keywords.items():
            if lexeme.startswith(keyword):
                return token_type
        
        # 妫€鏌ユ櫘閫氬叧閿瘝
        return self.keywords.get(lexeme)
    
    def _is_bai_jia_xing(self, lexeme: str) -> bool:
        """妫€鏌ユ槸鍚︿负鐧惧濮撳彉閲?""
        if not lexeme:
            return False
        
        # 鑾峰彇濮撴皬锛堢涓€涓瓧绗︼級
        surname = lexeme[0]
        
        # 妫€鏌ユ槸鍚︿负鍐茬獊濮撴皬
        if surname in self.conflict_surnames:
            return False
        
        # 妫€鏌ユ槸鍚︿负鐧惧濮?        return surname in self.bai_jia_xing
    
    def print_tokens(self, tokens: List[Token]) -> None:
        """鎵撳嵃璇嶆硶鍗曞厓鍒楄〃"""
        print("璇嶆硶鍒嗘瀽缁撴灉:")
        print("=" * 80)
        print(f"{'琛?:<4} {'鍒?:<4} {'绫诲瀷':<20} {'鍊?:<20} {'璇嶇礌':<20}")
        print("-" * 80)
        
        for token in tokens:
            value_str = str(token.value)
            if len(value_str) > 18:
                value_str = value_str[:15] + "..."
            
            lexeme_str = token.lexeme
            if len(lexeme_str) > 18:
                lexeme_str = lexeme_str[:15] + "..."
            
            print(f"{token.line:<4} {token.column:<4} {token.type.value:<20} {value_str:<20} {lexeme_str:<20}")
        
        print("=" * 80)


# 娴嬭瘯鍑芥暟
def test_lexer():
    """娴嬭瘯璇嶆硶鍒嗘瀽鍣?""
    print("璇嶆硶鍒嗘瀽鍣ㄦ祴璇?)
    print("=" * 50)
    
    lexer = YanLuLexer()
    
    # 娴嬭瘯鐢ㄤ緥
    test_cases = [
        (
            "瀹氭俯搴︽槸25銆?,
            "鍙橀噺瀹氫箟"
        ),
        (
            "濡傛灉娓╁害澶?0灏卞紑鍚鎵囥€?,
            "鏉′欢璇彞"
        ),
        (
            "瀵逛簬i鍦?鍒?0锛氬嵃i銆?,
            "寰幆璇彞"
        ),
        (
            "娓╁害鍙樹负30搴︺€?,
            "鐘舵€佽浆鎹?
        ),
        (
            "寮犱笁銆佹潕鍥涳紝璁＄畻鎶樻墸銆?,
            "鎰忓悎寮忓嚱鏁拌皟鐢?
        ),
        (
            "'浣犲ソ锛屼笘鐣?",
            "瀛楃涓插瓧闈㈤噺"
        ),
        (
            "鐪熶笖鍋?,
            "甯冨皵杩愮畻"
        ),
        (
            "瀹歺绛変簬鍗佸姞浜斻€?,
            "涓枃鏁板瓧"
        ),
    ]
    
    for source_code, description in test_cases:
        print(f"\n娴嬭瘯: {description}")
        print(f"婧愪唬鐮? {source_code}")
        
        try:
            tokens = lexer.tokenize(source_code)
            lexer.print_tokens(tokens)
        except Exception as e:
            print(f"閿欒: {e}")
    
    print("=" * 50)
    print("娴嬭瘯瀹屾垚")


if __name__ == "__main__":
    test_lexer())
    
    def _init_segmenter(self):
        """鍒濆鍖栧垎璇嶅櫒"""
        if self.segmenter_type == "thulac":
            try:
                import thulac
                # 浣跨敤seg_only=True鍙繘琛屽垎璇嶏紝涓嶈繘琛岃瘝鎬ф爣娉?                self.segmenter = thulac.thulac(seg_only=True, model_path=None)
                print(f"浣跨敤THULAC鍒嗚瘝鍣?(seg_only妯″紡)")
            except ImportError:
                print("璀﹀憡: 鏈畨瑁匱HULAC锛屽洖閫€鍒癹ieba鍒嗚瘝鍣?)
                print("瀹夎鍛戒护: pip install thulac")
                self.segmenter_type = "jieba"
                self.segmenter = jieba
        else:
            # 榛樿浣跨敤jieba
            self.segmenter = jieba
            print(f"浣跨敤jieba鍒嗚瘝鍣?)
    
    def _segment(self, text: str) -> List[str]:
        """
        鍒嗚瘝鏂规硶
        
        Args:
            text: 寰呭垎璇嶇殑鏂囨湰
            
        Returns:
            鍒嗚瘝缁撴灉鍒楄〃
        """
        if self.segmenter_type == "thulac":
            # THULAC鍒嗚瘝
            result = self.segmenter.cut(text, text=True)
            return result.split()
        else:
            # jieba鍒嗚瘝
            return list(self.segmenter.lcut(text))
        
    def tokenize(self, source_code: str) -> List[Token]:
        """
        灏嗘簮浠ｇ爜杞崲涓鸿瘝娉曞崟鍏冨垪琛?        
        Args:
            source_code: 婧愪唬鐮佸瓧绗︿覆
            
        Returns:
            璇嶆硶鍗曞厓鍒楄〃
        """
        tokens = []
        lines = source_code.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            line_tokens = self._tokenize_line(line, line_num)
            tokens.extend(line_tokens)
            
            # 娣诲姞鎹㈣绗︼紙闄ら潪鏄渶鍚庝竴琛岋級
            if line_num < len(lines):
                tokens.append(Token(TokenType.NEWLINE, '\n', line_num, len(line) + 1, '\n'))
        
        # 娣诲姞鏂囦欢缁撴潫鏍囪
        tokens.append(Token(TokenType.EOF, '', len(lines) + 1, 1, ''))
        
        return tokens
    
    def _tokenize_line(self, line: str, line_num: int) -> List[Token]:
        """灏嗕竴琛屼唬鐮佽浆鎹负璇嶆硶鍗曞厓鍒楄〃"""
        tokens = []
        position = 0
        column = 1
        
        # 浣跨敤鍒嗚瘝鍣ㄨ繘琛屼腑鏂囧垎璇?        segments = self._segment(line)
        segment_index = 0
        
        while position < len(line):
            # 璺宠繃绌虹櫧瀛楃
            if line[position].isspace():
                if line[position] == '\n':
                    tokens.append(Token(TokenType.NEWLINE, '\n', line_num, column, '\n'))
                position += 1
                column += 1
                continue
            
            # 澶勭悊娉ㄩ噴
            if line[position] == '#':
                # 鍗曡娉ㄩ噴锛岃烦杩囨暣琛?                comment = line[position:]
                tokens.append(Token(TokenType.COMMENT, comment, line_num, column, comment))
                break
            
            # 澶勭悊澶氳瑷€浠ｇ爜鍧?            if line[position:position+2] == '{{':
                tokens.append(Token(TokenType.CODE_BLOCK_START, '{{', line_num, column, '{{'))
                position += 2
                column += 2
                continue
            
            if line[position:position+2] == '}}':
                tokens.append(Token(TokenType.CODE_BLOCK_END, '}}', line_num, column, '}}'))
                position += 2
                column += 2
                continue
            
            # 澶勭悊涓枃鏍囩偣绗﹀彿
            if line[position] in self.chinese_punctuation:
                char = line[position]
                token_type = self.chinese_punctuation[char]
                
                # 澶勭悊鎴愬鏍囩偣绗﹀彿
                if char in ('銆?, '銆?):
                    # 鏌ユ壘鍖归厤鐨勭粨鏉熺鍙?                    end_pos = line.find('銆? if char == '銆? else '銆?, position + 1)
                    if end_pos != -1:
                        value = line[position:end_pos + 1]
                        tokens.append(Token(token_type, value, line_num, column, value))
                        position = end_pos + 1
                        column += len(value)
                        continue
                
                tokens.append(Token(token_type, char, line_num, column, char))
                position += 1
                column += 1
                continue
            
            # 澶勭悊鐪佺暐鍙?            if line[position:position+2] == '鈥︹€?:
                tokens.append(Token(TokenType.ELLIPSIS, '鈥︹€?, line_num, column, '鈥︹€?))
                position += 2
                column += 2
                continue
            
            # 澶勭悊鐮存姌鍙?            if line[position:position+2] == '鈥斺€?:
                tokens.append(Token(TokenType.DASH, '鈥斺€?, line_num, column, '鈥斺€?))
                position += 2
                column += 2
                continue
            
            # 澶勭悊鍦嗗湀鍙?            if line[position] in '鈶犫憽鈶⑩懀鈶も懃鈶︹懅鈶ㄢ懇':
                tokens.append(Token(TokenType.CIRCLED_NUMBERS, line[position], line_num, column, line[position]))
                position += 1
                column += 1
                continue
            
            # 澶勭悊杩愮畻绗?            if line[position] in self.operators:
                # 妫€鏌ュ弻瀛楃杩愮畻绗?                if position + 1 < len(line):
                    two_char = line[position:position+2]
                    if two_char in ('鈮?, '鈮?, '鈮?):
                        tokens.append(Token(self.operators[two_char], two_char, line_num, column, two_char))
                        position += 2
                        column += 2
                        continue
                
                tokens.append(Token(self.operators[line[position]], line[position], line_num, column, line[position]))
                position += 1
                column += 1
                continue
            
            # 澶勭悊鍒嗙粍绗﹀彿
            if line[position] in self.grouping_symbols:
                tokens.append(Token(self.grouping_symbols[line[position]], line[position], line_num, column, line[position]))
                position += 1
                column += 1
                continue
            
            # 澶勭悊瀛楃涓插瓧闈㈤噺
            if line[position] in ('"', "'"):
                string_token = self._parse_string_literal(line, position, line_num, column)
                tokens.append(string_token)
                position += len(string_token.lexeme)
                column += len(string_token.lexeme)
                continue
            
            # 澶勭悊鏁板瓧瀛楅潰閲?            if line[position].isdigit() or (line[position] == '.' and position + 1 < len(line) and line[position + 1].isdigit()):
                number_token = self._parse_number(line, position, line_num, column)
                tokens.append(number_token)
                position += len(number_token.lexeme)
                column += len(number_token.lexeme)
                continue
            
            # 澶勭悊涓枃鏁板瓧
            if line[position] in self.chinese_numbers:
                chinese_number_token = self._parse_chinese_number(line, position, line_num, column)
                tokens.append(chinese_number_token)
                position += len(chinese_number_token.lexeme)
                column += len(chinese_number_token.lexeme)
                continue
            
            # 澶勭悊褰撳墠鍒嗚瘝娈?            if segment_index < len(segments):
                segment = segments[segment_index].strip()
                if segment:  # 璺宠繃绌哄垎璇?                    # 澶勭悊鍒嗚瘝娈?                    token = self._process_segment(segment, line_num, column)
                    tokens.append(token)
                    position += len(segment)
                    column += len(segment)
                segment_index += 1
            else:
                # 濡傛灉娌℃湁鏇村鍒嗚瘝锛屽鐞嗗墿浣欏瓧绗?                identifier_token = self._parse_identifier(line, position, line_num, column)
                tokens.append(identifier_token)
                position += len(identifier_token.lexeme)
                column += len(identifier_token.lexeme)
        
        return tokens
    
    def _process_segment(self, segment: str, line_num: int, column: int) -> Token:
        """澶勭悊鍒嗚瘝娈?""
        # 妫€鏌ユ槸鍚︿负鍏抽敭璇?        token_type = self._get_keyword_type(segment)
        if token_type:
            return Token(token_type, segment, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负鐧惧濮撳彉閲?        if self._is_bai_jia_xing(segment):
            return Token(TokenType.BAIJIAXING, segment, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负鍔ㄨ瘝
        arity = get_verb_arity(segment)
        if arity != 0:
            # 鏍规嵁鍏冩暟纭畾鍔ㄨ瘝绫诲瀷
            if arity == -1:
                token_type = TokenType.VERB_VAR
            elif arity == 0:
                token_type = TokenType.VERB_0
            elif arity == 1:
                token_type = TokenType.VERB_1
            elif arity == 2:
                token_type = TokenType.VERB_2
            elif arity == 3:
                token_type = TokenType.VERB_3
            else:
                token_type = TokenType.VERB_VAR
            
            return Token(token_type, segment, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负甯冨皵瀛楅潰閲?        if segment in ('鐪?, '鍋?, 'true', 'false', 'True', 'False'):
            value = segment in ('鐪?, 'true', 'True')
            return Token(TokenType.BOOLEAN, value, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负绌哄€?        if segment == '绌?:
            return Token(TokenType.NULL, None, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负鏁板瓧
        if segment.isdigit() or (segment.replace('.', '', 1).isdigit() and segment.count('.') == 1):
            try:
                if '.' in segment:
                    value = float(segment)
                else:
                    value = int(segment)
                return Token(TokenType.NUMBER, value, line_num, column, segment)
            except ValueError:
                pass
        
        # 妫€鏌ユ槸鍚︿负涓枃鏁板瓧
        if all(c in self.chinese_numbers for c in segment):
            value = self._chinese_to_arabic(segment)
            return Token(TokenType.CHINESE_NUMBER, value, line_num, column, segment)
        
        # 鏅€氭爣璇嗙
        return Token(TokenType.IDENTIFIER, segment, line_num, column, segment)
    
    def _parse_string_literal(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽瀛楃涓插瓧闈㈤噺"""
        quote_char = line[start]
        position = start + 1
        value = ''
        
        while position < len(line):
            char = line[position]
            
            if char == quote_char:
                # 缁撴潫寮曞彿
                position += 1
                break
            elif char == '\\' and position + 1 < len(line):
                # 杞箟瀛楃
                next_char = line[position + 1]
                if next_char in ('n', 't', '\\', '"', "'"):
                    value += self._escape_char(next_char)
                    position += 2
                else:
                    value += char
                    position += 1
            else:
                value += char
                position += 1
        
        lexeme = line[start:position]
        return Token(TokenType.STRING, value, line_num, column, lexeme)
    
    def _escape_char(self, char: str) -> str:
        """杞箟瀛楃"""
        escape_map = {
            'n': '\n',
            't': '\t',
            '\\': '\\',
            '"': '"',
            "'": "'",
        }
        return escape_map.get(char, char)
    
    def _parse_number(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽鏁板瓧瀛楅潰閲?""
        position = start
        
        # 瑙ｆ瀽鏁存暟閮ㄥ垎
        while position < len(line) and line[position].isdigit():
            position += 1
        
        # 瑙ｆ瀽灏忔暟閮ㄥ垎
        if position < len(line) and line[position] == '.':
            position += 1
            while position < len(line) and line[position].isdigit():
                position += 1
        
        # 瑙ｆ瀽绉戝璁℃暟娉?        if position < len(line) and line[position].lower() == 'e':
            position += 1
            if position < len(line) and line[position] in ('+', '-'):
                position += 1
            while position < len(line) and line[position].isdigit():
                position += 1
        
        lexeme = line[start:position]
        
        # 灏濊瘯杞崲涓烘暟瀛?        try:
            if '.' in lexeme or 'e' in lexeme.lower():
                value = float(lexeme)
            else:
                value = int(lexeme)
        except ValueError:
            value = lexeme  # 淇濇寔鍘熸牱
        
        return Token(TokenType.NUMBER, value, line_num, column, lexeme)
    
    def _parse_chinese_number(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽涓枃鏁板瓧"""
        position = start
        lexeme = ''
        
        while position < len(line) and line[position] in self.chinese_numbers:
            lexeme += line[position]
            position += 1
        
        # 杞崲涓洪樋鎷変集鏁板瓧
        value = self._chinese_to_arabic(lexeme)
        
        return Token(TokenType.CHINESE_NUMBER, value, line_num, column, lexeme)
    
    def _chinese_to_arabic(self, chinese_num: str) -> int:
        """灏嗕腑鏂囨暟瀛楄浆鎹负闃挎媺浼暟瀛?""
        if not chinese_num:
            return 0
        
        # 绠€鍗曞疄鐜帮紝鍙鐞嗗熀鏈暟瀛?        total = 0
        current = 0
        
        for char in chinese_num:
            num = self.chinese_numbers.get(char, 0)
            
            if num < 10:
                current = num
            elif num >= 10:
                if current == 0:
                    current = 1
                total += current * num
                current = 0
        
        total += current
        return total
    
    def _parse_identifier(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽鏍囪瘑绗?""
        position = start
        
        # 鏀堕泦鏍囪瘑绗﹀瓧绗?        while position < len(line) and self._is_identifier_char(line[position]):
            position += 1
        
        lexeme = line[start:position]
        
        # 妫€鏌ユ槸鍚︿负鍏抽敭璇?        token_type = self._get_keyword_type(lexeme)
        if token_type:
            return Token(token_type, lexeme, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负鐧惧濮撳彉閲?        if self._is_bai_jia_xing(lexeme):
            return Token(TokenType.BAIJIAXING, lexeme, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负鍔ㄨ瘝
        arity = get_verb_arity(lexeme)
        if arity != 0:
            # 鏍规嵁鍏冩暟纭畾鍔ㄨ瘝绫诲瀷
            if arity == -1:
                token_type = TokenType.VERB_VAR
            elif arity == 0:
                token_type = TokenType.VERB_0
            elif arity == 1:
                token_type = TokenType.VERB_1
            elif arity == 2:
                token_type = TokenType.VERB_2
            elif arity == 3:
                token_type = TokenType.VERB_3
            else:
                token_type = TokenType.VERB_VAR
            
            return Token(token_type, lexeme, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负甯冨皵瀛楅潰閲?        if lexeme in ('鐪?, '鍋?, 'true', 'false', 'True', 'False'):
            value = lexeme in ('鐪?, 'true', 'True')
            return Token(TokenType.BOOLEAN, value, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负绌哄€?        if lexeme == '绌?:
            return Token(TokenType.NULL, None, line_num, column, lexeme)
        
        # 灏濊瘯涓枃鍒嗚瘝
        if len(lexeme) > 1 and any('\u4e00' <= c <= '\u9fff' for c in lexeme):
            # 浣跨敤jieba杩涜涓枃鍒嗚瘝
            segments = self._segment(lexeme)
            if len(segments) > 1:
                # 濡傛灉鏄涓瘝锛岃繑鍥炵涓€涓瘝浣滀负鏍囪瘑绗?                first_segment = segments[0]
                # 閫掑綊澶勭悊绗竴涓瘝
                return self._parse_identifier(first_segment, 0, line_num, column)
        
        # 鏅€氭爣璇嗙
        return Token(TokenType.IDENTIFIER, lexeme, line_num, column, lexeme)
    
    def _is_identifier_char(self, char: str) -> bool:
        """妫€鏌ュ瓧绗︽槸鍚︿负鏍囪瘑绗﹀瓧绗?""
        # 涓枃瀛楃銆佽嫳鏂囧瓧姣嶃€佹暟瀛椼€佷笅鍒掔嚎
        return ('\u4e00' <= char <= '\u9fff' or
                'a' <= char <= 'z' or
                'A' <= char <= 'Z' or
                char.isdigit() or
                char == '_')
    
    def _get_keyword_type(self, lexeme: str) -> Optional[TokenType]:
        """鑾峰彇鍏抽敭璇嶇被鍨?""
        # 妫€鏌ョ姸鎬佸叧閿瘝锛堝瀛楋級
        for keyword, token_type in self.state_keywords.items():
            if lexeme.startswith(keyword):
                return token_type
        
        # 妫€鏌ユ劅鐭ュ叧閿瘝锛堝瀛楋級
        for keyword, token_type in self.perception_keywords.items():
            if lexeme.startswith(keyword):
                return token_type
        
        # 妫€鏌ユ椂闂村叧閿瘝锛堝瀛楋級
        for keyword, token_type in self.time_keywords.items():
            if lexeme.startswith(keyword):
                return token_type
        
        # 妫€鏌ユ櫘閫氬叧閿瘝
        return self.keywords.get(lexeme)
    
    def _is_bai_jia_xing(self, lexeme: str) -> bool:
        """妫€鏌ユ槸鍚︿负鐧惧濮撳彉閲?""
        if not lexeme:
            return False
        
        # 鑾峰彇濮撴皬锛堢涓€涓瓧绗︼級
        surname = lexeme[0]
        
        # 妫€鏌ユ槸鍚︿负鍐茬獊濮撴皬
        if surname in self.conflict_surnames:
            return False
        
        # 妫€鏌ユ槸鍚︿负鐧惧濮?        return surname in self.bai_jia_xing
    
    def print_tokens(self, tokens: List[Token]) -> None:
        """鎵撳嵃璇嶆硶鍗曞厓鍒楄〃"""
        print("璇嶆硶鍒嗘瀽缁撴灉:")
        print("=" * 80)
        print(f"{'琛?:<4} {'鍒?:<4} {'绫诲瀷':<20} {'鍊?:<20} {'璇嶇礌':<20}")
        print("-" * 80)
        
        for token in tokens:
            value_str = str(token.value)
            if len(value_str) > 18:
                value_str = value_str[:15] + "..."
            
            lexeme_str = token.lexeme
            if len(lexeme_str) > 18:
                lexeme_str = lexeme_str[:15] + "..."
            
            print(f"{token.line:<4} {token.column:<4} {token.type.value:<20} {value_str:<20} {lexeme_str:<20}")
        
        print("=" * 80)


# 娴嬭瘯鍑芥暟
def test_lexer():
    """娴嬭瘯璇嶆硶鍒嗘瀽鍣?""
    print("璇嶆硶鍒嗘瀽鍣ㄦ祴璇?)
    print("=" * 50)
    
    lexer = YanLuLexer()
    
    # 娴嬭瘯鐢ㄤ緥
    test_cases = [
        (
            "瀹氭俯搴︽槸25銆?,
            "鍙橀噺瀹氫箟"
        ),
        (
            "濡傛灉娓╁害澶?0灏卞紑鍚鎵囥€?,
            "鏉′欢璇彞"
        ),
        (
            "瀵逛簬i鍦?鍒?0锛氬嵃i銆?,
            "寰幆璇彞"
        ),
        (
            "娓╁害鍙樹负30搴︺€?,
            "鐘舵€佽浆鎹?
        ),
        (
            "寮犱笁銆佹潕鍥涳紝璁＄畻鎶樻墸銆?,
            "鎰忓悎寮忓嚱鏁拌皟鐢?
        ),
        (
            "'浣犲ソ锛屼笘鐣?",
            "瀛楃涓插瓧闈㈤噺"
        ),
        (
            "鐪熶笖鍋?,
            "甯冨皵杩愮畻"
        ),
        (
            "瀹歺绛変簬鍗佸姞浜斻€?,
            "涓枃鏁板瓧"
        ),
    ]
    
    for source_code, description in test_cases:
        print(f"\n娴嬭瘯: {description}")
        print(f"婧愪唬鐮? {source_code}")
        
        try:
            tokens = lexer.tokenize(source_code)
            lexer.print_tokens(tokens)
        except Exception as e:
            print(f"閿欒: {e}")
    
    print("=" * 50)
    print("娴嬭瘯瀹屾垚")


if __name__ == "__main__":
    test_lexer())
        self.identifier_pattern = re.compile(r'^[\u4e00-\u9fffA-Za-z_][\u4e00-\u9fffA-Za-z0-9_]*
        """
        灏嗘簮浠ｇ爜杞崲涓鸿瘝娉曞崟鍏冨垪琛?        
        Args:
            source_code: 婧愪唬鐮佸瓧绗︿覆
            
        Returns:
            璇嶆硶鍗曞厓鍒楄〃
        """
        tokens = []
        lines = source_code.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            line_tokens = self._tokenize_line(line, line_num)
            tokens.extend(line_tokens)
            
            # 娣诲姞鎹㈣绗︼紙闄ら潪鏄渶鍚庝竴琛岋級
            if line_num < len(lines):
                tokens.append(Token(TokenType.NEWLINE, '\n', line_num, len(line) + 1, '\n'))
        
        # 娣诲姞鏂囦欢缁撴潫鏍囪
        tokens.append(Token(TokenType.EOF, '', len(lines) + 1, 1, ''))
        
        return tokens
    
    def _tokenize_line(self, line: str, line_num: int) -> List[Token]:
        """灏嗕竴琛屼唬鐮佽浆鎹负璇嶆硶鍗曞厓鍒楄〃"""
        tokens = []
        position = 0
        column = 1
        
        # 浣跨敤鍒嗚瘝鍣ㄨ繘琛屼腑鏂囧垎璇?        segments = self._segment(line)
        segment_index = 0
        
        while position < len(line):
            # 璺宠繃绌虹櫧瀛楃
            if line[position].isspace():
                if line[position] == '\n':
                    tokens.append(Token(TokenType.NEWLINE, '\n', line_num, column, '\n'))
                position += 1
                column += 1
                continue
            
            # 澶勭悊娉ㄩ噴
            if line[position] == '#':
                # 鍗曡娉ㄩ噴锛岃烦杩囨暣琛?                comment = line[position:]
                tokens.append(Token(TokenType.COMMENT, comment, line_num, column, comment))
                break
            
            # 澶勭悊澶氳瑷€浠ｇ爜鍧?            if line[position:position+2] == '{{':
                tokens.append(Token(TokenType.CODE_BLOCK_START, '{{', line_num, column, '{{'))
                position += 2
                column += 2
                continue
            
            if line[position:position+2] == '}}':
                tokens.append(Token(TokenType.CODE_BLOCK_END, '}}', line_num, column, '}}'))
                position += 2
                column += 2
                continue
            
            # 澶勭悊涓枃鏍囩偣绗﹀彿
            if line[position] in self.chinese_punctuation:
                char = line[position]
                token_type = self.chinese_punctuation[char]
                
                # 澶勭悊鎴愬鏍囩偣绗﹀彿
                if char in ('銆?, '銆?):
                    # 鏌ユ壘鍖归厤鐨勭粨鏉熺鍙?                    end_pos = line.find('銆? if char == '銆? else '銆?, position + 1)
                    if end_pos != -1:
                        value = line[position:end_pos + 1]
                        tokens.append(Token(token_type, value, line_num, column, value))
                        position = end_pos + 1
                        column += len(value)
                        continue
                
                tokens.append(Token(token_type, char, line_num, column, char))
                position += 1
                column += 1
                continue
            
            # 澶勭悊鐪佺暐鍙?            if line[position:position+2] == '鈥︹€?:
                tokens.append(Token(TokenType.ELLIPSIS, '鈥︹€?, line_num, column, '鈥︹€?))
                position += 2
                column += 2
                continue
            
            # 澶勭悊鐮存姌鍙?            if line[position:position+2] == '鈥斺€?:
                tokens.append(Token(TokenType.DASH, '鈥斺€?, line_num, column, '鈥斺€?))
                position += 2
                column += 2
                continue
            
            # 澶勭悊鍦嗗湀鍙?            if line[position] in '鈶犫憽鈶⑩懀鈶も懃鈶︹懅鈶ㄢ懇':
                tokens.append(Token(TokenType.CIRCLED_NUMBERS, line[position], line_num, column, line[position]))
                position += 1
                column += 1
                continue
            
            # 澶勭悊杩愮畻绗?            if line[position] in self.operators:
                # 妫€鏌ュ弻瀛楃杩愮畻绗?                if position + 1 < len(line):
                    two_char = line[position:position+2]
                    if two_char in ('鈮?, '鈮?, '鈮?):
                        tokens.append(Token(self.operators[two_char], two_char, line_num, column, two_char))
                        position += 2
                        column += 2
                        continue
                
                tokens.append(Token(self.operators[line[position]], line[position], line_num, column, line[position]))
                position += 1
                column += 1
                continue
            
            # 澶勭悊鍒嗙粍绗﹀彿
            if line[position] in self.grouping_symbols:
                tokens.append(Token(self.grouping_symbols[line[position]], line[position], line_num, column, line[position]))
                position += 1
                column += 1
                continue
            
            # 澶勭悊瀛楃涓插瓧闈㈤噺
            if line[position] in ('"', "'"):
                string_token = self._parse_string_literal(line, position, line_num, column)
                tokens.append(string_token)
                position += len(string_token.lexeme)
                column += len(string_token.lexeme)
                continue
            
            # 澶勭悊鏁板瓧瀛楅潰閲?            if line[position].isdigit() or (line[position] == '.' and position + 1 < len(line) and line[position + 1].isdigit()):
                number_token = self._parse_number(line, position, line_num, column)
                tokens.append(number_token)
                position += len(number_token.lexeme)
                column += len(number_token.lexeme)
                continue
            
            # 澶勭悊涓枃鏁板瓧
            if line[position] in self.chinese_numbers:
                chinese_number_token = self._parse_chinese_number(line, position, line_num, column)
                tokens.append(chinese_number_token)
                position += len(chinese_number_token.lexeme)
                column += len(chinese_number_token.lexeme)
                continue
            
            # 澶勭悊褰撳墠鍒嗚瘝娈?            if segment_index < len(segments):
                segment = segments[segment_index].strip()
                if segment:  # 璺宠繃绌哄垎璇?                    # 澶勭悊鍒嗚瘝娈?                    token = self._process_segment(segment, line_num, column)
                    tokens.append(token)
                    position += len(segment)
                    column += len(segment)
                segment_index += 1
            else:
                # 濡傛灉娌℃湁鏇村鍒嗚瘝锛屽鐞嗗墿浣欏瓧绗?                identifier_token = self._parse_identifier(line, position, line_num, column)
                tokens.append(identifier_token)
                position += len(identifier_token.lexeme)
                column += len(identifier_token.lexeme)
        
        return tokens
    
    def _process_segment(self, segment: str, line_num: int, column: int) -> Token:
        """澶勭悊鍒嗚瘝娈?""
        # 妫€鏌ユ槸鍚︿负鍏抽敭璇?        token_type = self._get_keyword_type(segment)
        if token_type:
            return Token(token_type, segment, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负鐧惧濮撳彉閲?        if self._is_bai_jia_xing(segment):
            return Token(TokenType.BAIJIAXING, segment, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负鍔ㄨ瘝
        arity = get_verb_arity(segment)
        if arity != 0:
            # 鏍规嵁鍏冩暟纭畾鍔ㄨ瘝绫诲瀷
            if arity == -1:
                token_type = TokenType.VERB_VAR
            elif arity == 0:
                token_type = TokenType.VERB_0
            elif arity == 1:
                token_type = TokenType.VERB_1
            elif arity == 2:
                token_type = TokenType.VERB_2
            elif arity == 3:
                token_type = TokenType.VERB_3
            else:
                token_type = TokenType.VERB_VAR
            
            return Token(token_type, segment, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负甯冨皵瀛楅潰閲?        if segment in ('鐪?, '鍋?, 'true', 'false', 'True', 'False'):
            value = segment in ('鐪?, 'true', 'True')
            return Token(TokenType.BOOLEAN, value, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负绌哄€?        if segment == '绌?:
            return Token(TokenType.NULL, None, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负鏁板瓧
        if segment.isdigit() or (segment.replace('.', '', 1).isdigit() and segment.count('.') == 1):
            try:
                if '.' in segment:
                    value = float(segment)
                else:
                    value = int(segment)
                return Token(TokenType.NUMBER, value, line_num, column, segment)
            except ValueError:
                pass
        
        # 妫€鏌ユ槸鍚︿负涓枃鏁板瓧
        if all(c in self.chinese_numbers for c in segment):
            value = self._chinese_to_arabic(segment)
            return Token(TokenType.CHINESE_NUMBER, value, line_num, column, segment)
        
        # 鏅€氭爣璇嗙
        return Token(TokenType.IDENTIFIER, segment, line_num, column, segment)
    
    def _parse_string_literal(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽瀛楃涓插瓧闈㈤噺"""
        quote_char = line[start]
        position = start + 1
        value = ''
        
        while position < len(line):
            char = line[position]
            
            if char == quote_char:
                # 缁撴潫寮曞彿
                position += 1
                break
            elif char == '\\' and position + 1 < len(line):
                # 杞箟瀛楃
                next_char = line[position + 1]
                if next_char in ('n', 't', '\\', '"', "'"):
                    value += self._escape_char(next_char)
                    position += 2
                else:
                    value += char
                    position += 1
            else:
                value += char
                position += 1
        
        lexeme = line[start:position]
        return Token(TokenType.STRING, value, line_num, column, lexeme)
    
    def _escape_char(self, char: str) -> str:
        """杞箟瀛楃"""
        escape_map = {
            'n': '\n',
            't': '\t',
            '\\': '\\',
            '"': '"',
            "'": "'",
        }
        return escape_map.get(char, char)
    
    def _parse_number(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽鏁板瓧瀛楅潰閲?""
        position = start
        
        # 瑙ｆ瀽鏁存暟閮ㄥ垎
        while position < len(line) and line[position].isdigit():
            position += 1
        
        # 瑙ｆ瀽灏忔暟閮ㄥ垎
        if position < len(line) and line[position] == '.':
            position += 1
            while position < len(line) and line[position].isdigit():
                position += 1
        
        # 瑙ｆ瀽绉戝璁℃暟娉?        if position < len(line) and line[position].lower() == 'e':
            position += 1
            if position < len(line) and line[position] in ('+', '-'):
                position += 1
            while position < len(line) and line[position].isdigit():
                position += 1
        
        lexeme = line[start:position]
        
        # 灏濊瘯杞崲涓烘暟瀛?        try:
            if '.' in lexeme or 'e' in lexeme.lower():
                value = float(lexeme)
            else:
                value = int(lexeme)
        except ValueError:
            value = lexeme  # 淇濇寔鍘熸牱
        
        return Token(TokenType.NUMBER, value, line_num, column, lexeme)
    
    def _parse_chinese_number(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽涓枃鏁板瓧"""
        position = start
        lexeme = ''
        
        while position < len(line) and line[position] in self.chinese_numbers:
            lexeme += line[position]
            position += 1
        
        # 杞崲涓洪樋鎷変集鏁板瓧
        value = self._chinese_to_arabic(lexeme)
        
        return Token(TokenType.CHINESE_NUMBER, value, line_num, column, lexeme)
    
    def _chinese_to_arabic(self, chinese_num: str) -> int:
        """灏嗕腑鏂囨暟瀛楄浆鎹负闃挎媺浼暟瀛?""
        if not chinese_num:
            return 0
        
        # 绠€鍗曞疄鐜帮紝鍙鐞嗗熀鏈暟瀛?        total = 0
        current = 0
        
        for char in chinese_num:
            num = self.chinese_numbers.get(char, 0)
            
            if num < 10:
                current = num
            elif num >= 10:
                if current == 0:
                    current = 1
                total += current * num
                current = 0
        
        total += current
        return total
    
    def _parse_identifier(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽鏍囪瘑绗?""
        position = start
        
        # 鏀堕泦鏍囪瘑绗﹀瓧绗?        while position < len(line) and self._is_identifier_char(line[position]):
            position += 1
        
        lexeme = line[start:position]
        
        # 妫€鏌ユ槸鍚︿负鍏抽敭璇?        token_type = self._get_keyword_type(lexeme)
        if token_type:
            return Token(token_type, lexeme, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负鐧惧濮撳彉閲?        if self._is_bai_jia_xing(lexeme):
            return Token(TokenType.BAIJIAXING, lexeme, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负鍔ㄨ瘝
        arity = get_verb_arity(lexeme)
        if arity != 0:
            # 鏍规嵁鍏冩暟纭畾鍔ㄨ瘝绫诲瀷
            if arity == -1:
                token_type = TokenType.VERB_VAR
            elif arity == 0:
                token_type = TokenType.VERB_0
            elif arity == 1:
                token_type = TokenType.VERB_1
            elif arity == 2:
                token_type = TokenType.VERB_2
            elif arity == 3:
                token_type = TokenType.VERB_3
            else:
                token_type = TokenType.VERB_VAR
            
            return Token(token_type, lexeme, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负甯冨皵瀛楅潰閲?        if lexeme in ('鐪?, '鍋?, 'true', 'false', 'True', 'False'):
            value = lexeme in ('鐪?, 'true', 'True')
            return Token(TokenType.BOOLEAN, value, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负绌哄€?        if lexeme == '绌?:
            return Token(TokenType.NULL, None, line_num, column, lexeme)
        
        # 灏濊瘯涓枃鍒嗚瘝
        if len(lexeme) > 1 and any('\u4e00' <= c <= '\u9fff' for c in lexeme):
            # 浣跨敤jieba杩涜涓枃鍒嗚瘝
            segments = self._segment(lexeme)
            if len(segments) > 1:
                # 濡傛灉鏄涓瘝锛岃繑鍥炵涓€涓瘝浣滀负鏍囪瘑绗?                first_segment = segments[0]
                # 閫掑綊澶勭悊绗竴涓瘝
                return self._parse_identifier(first_segment, 0, line_num, column)
        
        # 鏅€氭爣璇嗙
        return Token(TokenType.IDENTIFIER, lexeme, line_num, column, lexeme)
    
    def _is_identifier_char(self, char: str) -> bool:
        """妫€鏌ュ瓧绗︽槸鍚︿负鏍囪瘑绗﹀瓧绗?""
        # 涓枃瀛楃銆佽嫳鏂囧瓧姣嶃€佹暟瀛椼€佷笅鍒掔嚎
        return ('\u4e00' <= char <= '\u9fff' or
                'a' <= char <= 'z' or
                'A' <= char <= 'Z' or
                char.isdigit() or
                char == '_')
    
    def _get_keyword_type(self, lexeme: str) -> Optional[TokenType]:
        """鑾峰彇鍏抽敭璇嶇被鍨?""
        # 妫€鏌ョ姸鎬佸叧閿瘝锛堝瀛楋級
        for keyword, token_type in self.state_keywords.items():
            if lexeme.startswith(keyword):
                return token_type
        
        # 妫€鏌ユ劅鐭ュ叧閿瘝锛堝瀛楋級
        for keyword, token_type in self.perception_keywords.items():
            if lexeme.startswith(keyword):
                return token_type
        
        # 妫€鏌ユ椂闂村叧閿瘝锛堝瀛楋級
        for keyword, token_type in self.time_keywords.items():
            if lexeme.startswith(keyword):
                return token_type
        
        # 妫€鏌ユ櫘閫氬叧閿瘝
        return self.keywords.get(lexeme)
    
    def _is_bai_jia_xing(self, lexeme: str) -> bool:
        """妫€鏌ユ槸鍚︿负鐧惧濮撳彉閲?""
        if not lexeme:
            return False
        
        # 鑾峰彇濮撴皬锛堢涓€涓瓧绗︼級
        surname = lexeme[0]
        
        # 妫€鏌ユ槸鍚︿负鍐茬獊濮撴皬
        if surname in self.conflict_surnames:
            return False
        
        # 妫€鏌ユ槸鍚︿负鐧惧濮?        return surname in self.bai_jia_xing
    
    def print_tokens(self, tokens: List[Token]) -> None:
        """鎵撳嵃璇嶆硶鍗曞厓鍒楄〃"""
        print("璇嶆硶鍒嗘瀽缁撴灉:")
        print("=" * 80)
        print(f"{'琛?:<4} {'鍒?:<4} {'绫诲瀷':<20} {'鍊?:<20} {'璇嶇礌':<20}")
        print("-" * 80)
        
        for token in tokens:
            value_str = str(token.value)
            if len(value_str) > 18:
                value_str = value_str[:15] + "..."
            
            lexeme_str = token.lexeme
            if len(lexeme_str) > 18:
                lexeme_str = lexeme_str[:15] + "..."
            
            print(f"{token.line:<4} {token.column:<4} {token.type.value:<20} {value_str:<20} {lexeme_str:<20}")
        
        print("=" * 80)


# 娴嬭瘯鍑芥暟
def test_lexer():
    """娴嬭瘯璇嶆硶鍒嗘瀽鍣?""
    print("璇嶆硶鍒嗘瀽鍣ㄦ祴璇?)
    print("=" * 50)
    
    lexer = YanLuLexer()
    
    # 娴嬭瘯鐢ㄤ緥
    test_cases = [
        (
            "瀹氭俯搴︽槸25銆?,
            "鍙橀噺瀹氫箟"
        ),
        (
            "濡傛灉娓╁害澶?0灏卞紑鍚鎵囥€?,
            "鏉′欢璇彞"
        ),
        (
            "瀵逛簬i鍦?鍒?0锛氬嵃i銆?,
            "寰幆璇彞"
        ),
        (
            "娓╁害鍙樹负30搴︺€?,
            "鐘舵€佽浆鎹?
        ),
        (
            "寮犱笁銆佹潕鍥涳紝璁＄畻鎶樻墸銆?,
            "鎰忓悎寮忓嚱鏁拌皟鐢?
        ),
        (
            "'浣犲ソ锛屼笘鐣?",
            "瀛楃涓插瓧闈㈤噺"
        ),
        (
            "鐪熶笖鍋?,
            "甯冨皵杩愮畻"
        ),
        (
            "瀹歺绛変簬鍗佸姞浜斻€?,
            "涓枃鏁板瓧"
        ),
    ]
    
    for source_code, description in test_cases:
        print(f"\n娴嬭瘯: {description}")
        print(f"婧愪唬鐮? {source_code}")
        
        try:
            tokens = lexer.tokenize(source_code)
            lexer.print_tokens(tokens)
        except Exception as e:
            print(f"閿欒: {e}")
    
    print("=" * 50)
    print("娴嬭瘯瀹屾垚")


if __name__ == "__main__":
    test_lexer())
    
    def _init_segmenter(self):
        """鍒濆鍖栧垎璇嶅櫒"""
        if self.segmenter_type == "thulac":
            try:
                import thulac
                # 浣跨敤seg_only=True鍙繘琛屽垎璇嶏紝涓嶈繘琛岃瘝鎬ф爣娉?                self.segmenter = thulac.thulac(seg_only=True, model_path=None)
                print(f"浣跨敤THULAC鍒嗚瘝鍣?(seg_only妯″紡)")
            except ImportError:
                print("璀﹀憡: 鏈畨瑁匱HULAC锛屽洖閫€鍒癹ieba鍒嗚瘝鍣?)
                print("瀹夎鍛戒护: pip install thulac")
                self.segmenter_type = "jieba"
                self.segmenter = jieba
        else:
            # 榛樿浣跨敤jieba
            self.segmenter = jieba
            print(f"浣跨敤jieba鍒嗚瘝鍣?)
    
    def _segment(self, text: str) -> List[str]:
        """
        鍒嗚瘝鏂规硶
        
        Args:
            text: 寰呭垎璇嶇殑鏂囨湰
            
        Returns:
            鍒嗚瘝缁撴灉鍒楄〃
        """
        if self.segmenter_type == "thulac":
            # THULAC鍒嗚瘝
            result = self.segmenter.cut(text, text=True)
            return result.split()
        else:
            # jieba鍒嗚瘝
            return list(self.segmenter.lcut(text))
        
    def tokenize(self, source_code: str) -> List[Token]:
        """
        灏嗘簮浠ｇ爜杞崲涓鸿瘝娉曞崟鍏冨垪琛?        
        Args:
            source_code: 婧愪唬鐮佸瓧绗︿覆
            
        Returns:
            璇嶆硶鍗曞厓鍒楄〃
        """
        tokens = []
        lines = source_code.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            line_tokens = self._tokenize_line(line, line_num)
            tokens.extend(line_tokens)
            
            # 娣诲姞鎹㈣绗︼紙闄ら潪鏄渶鍚庝竴琛岋級
            if line_num < len(lines):
                tokens.append(Token(TokenType.NEWLINE, '\n', line_num, len(line) + 1, '\n'))
        
        # 娣诲姞鏂囦欢缁撴潫鏍囪
        tokens.append(Token(TokenType.EOF, '', len(lines) + 1, 1, ''))
        
        return tokens
    
    def _tokenize_line(self, line: str, line_num: int) -> List[Token]:
        """灏嗕竴琛屼唬鐮佽浆鎹负璇嶆硶鍗曞厓鍒楄〃"""
        tokens = []
        position = 0
        column = 1
        
        # 浣跨敤鍒嗚瘝鍣ㄨ繘琛屼腑鏂囧垎璇?        segments = self._segment(line)
        segment_index = 0
        
        while position < len(line):
            # 璺宠繃绌虹櫧瀛楃
            if line[position].isspace():
                if line[position] == '\n':
                    tokens.append(Token(TokenType.NEWLINE, '\n', line_num, column, '\n'))
                position += 1
                column += 1
                continue
            
            # 澶勭悊娉ㄩ噴
            if line[position] == '#':
                # 鍗曡娉ㄩ噴锛岃烦杩囨暣琛?                comment = line[position:]
                tokens.append(Token(TokenType.COMMENT, comment, line_num, column, comment))
                break
            
            # 澶勭悊澶氳瑷€浠ｇ爜鍧?            if line[position:position+2] == '{{':
                tokens.append(Token(TokenType.CODE_BLOCK_START, '{{', line_num, column, '{{'))
                position += 2
                column += 2
                continue
            
            if line[position:position+2] == '}}':
                tokens.append(Token(TokenType.CODE_BLOCK_END, '}}', line_num, column, '}}'))
                position += 2
                column += 2
                continue
            
            # 澶勭悊涓枃鏍囩偣绗﹀彿
            if line[position] in self.chinese_punctuation:
                char = line[position]
                token_type = self.chinese_punctuation[char]
                
                # 澶勭悊鎴愬鏍囩偣绗﹀彿
                if char in ('銆?, '銆?):
                    # 鏌ユ壘鍖归厤鐨勭粨鏉熺鍙?                    end_pos = line.find('銆? if char == '銆? else '銆?, position + 1)
                    if end_pos != -1:
                        value = line[position:end_pos + 1]
                        tokens.append(Token(token_type, value, line_num, column, value))
                        position = end_pos + 1
                        column += len(value)
                        continue
                
                tokens.append(Token(token_type, char, line_num, column, char))
                position += 1
                column += 1
                continue
            
            # 澶勭悊鐪佺暐鍙?            if line[position:position+2] == '鈥︹€?:
                tokens.append(Token(TokenType.ELLIPSIS, '鈥︹€?, line_num, column, '鈥︹€?))
                position += 2
                column += 2
                continue
            
            # 澶勭悊鐮存姌鍙?            if line[position:position+2] == '鈥斺€?:
                tokens.append(Token(TokenType.DASH, '鈥斺€?, line_num, column, '鈥斺€?))
                position += 2
                column += 2
                continue
            
            # 澶勭悊鍦嗗湀鍙?            if line[position] in '鈶犫憽鈶⑩懀鈶も懃鈶︹懅鈶ㄢ懇':
                tokens.append(Token(TokenType.CIRCLED_NUMBERS, line[position], line_num, column, line[position]))
                position += 1
                column += 1
                continue
            
            # 澶勭悊杩愮畻绗?            if line[position] in self.operators:
                # 妫€鏌ュ弻瀛楃杩愮畻绗?                if position + 1 < len(line):
                    two_char = line[position:position+2]
                    if two_char in ('鈮?, '鈮?, '鈮?):
                        tokens.append(Token(self.operators[two_char], two_char, line_num, column, two_char))
                        position += 2
                        column += 2
                        continue
                
                tokens.append(Token(self.operators[line[position]], line[position], line_num, column, line[position]))
                position += 1
                column += 1
                continue
            
            # 澶勭悊鍒嗙粍绗﹀彿
            if line[position] in self.grouping_symbols:
                tokens.append(Token(self.grouping_symbols[line[position]], line[position], line_num, column, line[position]))
                position += 1
                column += 1
                continue
            
            # 澶勭悊瀛楃涓插瓧闈㈤噺
            if line[position] in ('"', "'"):
                string_token = self._parse_string_literal(line, position, line_num, column)
                tokens.append(string_token)
                position += len(string_token.lexeme)
                column += len(string_token.lexeme)
                continue
            
            # 澶勭悊鏁板瓧瀛楅潰閲?            if line[position].isdigit() or (line[position] == '.' and position + 1 < len(line) and line[position + 1].isdigit()):
                number_token = self._parse_number(line, position, line_num, column)
                tokens.append(number_token)
                position += len(number_token.lexeme)
                column += len(number_token.lexeme)
                continue
            
            # 澶勭悊涓枃鏁板瓧
            if line[position] in self.chinese_numbers:
                chinese_number_token = self._parse_chinese_number(line, position, line_num, column)
                tokens.append(chinese_number_token)
                position += len(chinese_number_token.lexeme)
                column += len(chinese_number_token.lexeme)
                continue
            
            # 澶勭悊褰撳墠鍒嗚瘝娈?            if segment_index < len(segments):
                segment = segments[segment_index].strip()
                if segment:  # 璺宠繃绌哄垎璇?                    # 澶勭悊鍒嗚瘝娈?                    token = self._process_segment(segment, line_num, column)
                    tokens.append(token)
                    position += len(segment)
                    column += len(segment)
                segment_index += 1
            else:
                # 濡傛灉娌℃湁鏇村鍒嗚瘝锛屽鐞嗗墿浣欏瓧绗?                identifier_token = self._parse_identifier(line, position, line_num, column)
                tokens.append(identifier_token)
                position += len(identifier_token.lexeme)
                column += len(identifier_token.lexeme)
        
        return tokens
    
    def _process_segment(self, segment: str, line_num: int, column: int) -> Token:
        """澶勭悊鍒嗚瘝娈?""
        # 妫€鏌ユ槸鍚︿负鍏抽敭璇?        token_type = self._get_keyword_type(segment)
        if token_type:
            return Token(token_type, segment, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负鐧惧濮撳彉閲?        if self._is_bai_jia_xing(segment):
            return Token(TokenType.BAIJIAXING, segment, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负鍔ㄨ瘝
        arity = get_verb_arity(segment)
        if arity != 0:
            # 鏍规嵁鍏冩暟纭畾鍔ㄨ瘝绫诲瀷
            if arity == -1:
                token_type = TokenType.VERB_VAR
            elif arity == 0:
                token_type = TokenType.VERB_0
            elif arity == 1:
                token_type = TokenType.VERB_1
            elif arity == 2:
                token_type = TokenType.VERB_2
            elif arity == 3:
                token_type = TokenType.VERB_3
            else:
                token_type = TokenType.VERB_VAR
            
            return Token(token_type, segment, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负甯冨皵瀛楅潰閲?        if segment in ('鐪?, '鍋?, 'true', 'false', 'True', 'False'):
            value = segment in ('鐪?, 'true', 'True')
            return Token(TokenType.BOOLEAN, value, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负绌哄€?        if segment == '绌?:
            return Token(TokenType.NULL, None, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负鏁板瓧
        if segment.isdigit() or (segment.replace('.', '', 1).isdigit() and segment.count('.') == 1):
            try:
                if '.' in segment:
                    value = float(segment)
                else:
                    value = int(segment)
                return Token(TokenType.NUMBER, value, line_num, column, segment)
            except ValueError:
                pass
        
        # 妫€鏌ユ槸鍚︿负涓枃鏁板瓧
        if all(c in self.chinese_numbers for c in segment):
            value = self._chinese_to_arabic(segment)
            return Token(TokenType.CHINESE_NUMBER, value, line_num, column, segment)
        
        # 鏅€氭爣璇嗙
        return Token(TokenType.IDENTIFIER, segment, line_num, column, segment)
    
    def _parse_string_literal(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽瀛楃涓插瓧闈㈤噺"""
        quote_char = line[start]
        position = start + 1
        value = ''
        
        while position < len(line):
            char = line[position]
            
            if char == quote_char:
                # 缁撴潫寮曞彿
                position += 1
                break
            elif char == '\\' and position + 1 < len(line):
                # 杞箟瀛楃
                next_char = line[position + 1]
                if next_char in ('n', 't', '\\', '"', "'"):
                    value += self._escape_char(next_char)
                    position += 2
                else:
                    value += char
                    position += 1
            else:
                value += char
                position += 1
        
        lexeme = line[start:position]
        return Token(TokenType.STRING, value, line_num, column, lexeme)
    
    def _escape_char(self, char: str) -> str:
        """杞箟瀛楃"""
        escape_map = {
            'n': '\n',
            't': '\t',
            '\\': '\\',
            '"': '"',
            "'": "'",
        }
        return escape_map.get(char, char)
    
    def _parse_number(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽鏁板瓧瀛楅潰閲?""
        position = start
        
        # 瑙ｆ瀽鏁存暟閮ㄥ垎
        while position < len(line) and line[position].isdigit():
            position += 1
        
        # 瑙ｆ瀽灏忔暟閮ㄥ垎
        if position < len(line) and line[position] == '.':
            position += 1
            while position < len(line) and line[position].isdigit():
                position += 1
        
        # 瑙ｆ瀽绉戝璁℃暟娉?        if position < len(line) and line[position].lower() == 'e':
            position += 1
            if position < len(line) and line[position] in ('+', '-'):
                position += 1
            while position < len(line) and line[position].isdigit():
                position += 1
        
        lexeme = line[start:position]
        
        # 灏濊瘯杞崲涓烘暟瀛?        try:
            if '.' in lexeme or 'e' in lexeme.lower():
                value = float(lexeme)
            else:
                value = int(lexeme)
        except ValueError:
            value = lexeme  # 淇濇寔鍘熸牱
        
        return Token(TokenType.NUMBER, value, line_num, column, lexeme)
    
    def _parse_chinese_number(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽涓枃鏁板瓧"""
        position = start
        lexeme = ''
        
        while position < len(line) and line[position] in self.chinese_numbers:
            lexeme += line[position]
            position += 1
        
        # 杞崲涓洪樋鎷変集鏁板瓧
        value = self._chinese_to_arabic(lexeme)
        
        return Token(TokenType.CHINESE_NUMBER, value, line_num, column, lexeme)
    
    def _chinese_to_arabic(self, chinese_num: str) -> int:
        """灏嗕腑鏂囨暟瀛楄浆鎹负闃挎媺浼暟瀛?""
        if not chinese_num:
            return 0
        
        # 绠€鍗曞疄鐜帮紝鍙鐞嗗熀鏈暟瀛?        total = 0
        current = 0
        
        for char in chinese_num:
            num = self.chinese_numbers.get(char, 0)
            
            if num < 10:
                current = num
            elif num >= 10:
                if current == 0:
                    current = 1
                total += current * num
                current = 0
        
        total += current
        return total
    
    def _parse_identifier(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽鏍囪瘑绗?""
        position = start
        
        # 鏀堕泦鏍囪瘑绗﹀瓧绗?        while position < len(line) and self._is_identifier_char(line[position]):
            position += 1
        
        lexeme = line[start:position]
        
        # 妫€鏌ユ槸鍚︿负鍏抽敭璇?        token_type = self._get_keyword_type(lexeme)
        if token_type:
            return Token(token_type, lexeme, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负鐧惧濮撳彉閲?        if self._is_bai_jia_xing(lexeme):
            return Token(TokenType.BAIJIAXING, lexeme, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负鍔ㄨ瘝
        arity = get_verb_arity(lexeme)
        if arity != 0:
            # 鏍规嵁鍏冩暟纭畾鍔ㄨ瘝绫诲瀷
            if arity == -1:
                token_type = TokenType.VERB_VAR
            elif arity == 0:
                token_type = TokenType.VERB_0
            elif arity == 1:
                token_type = TokenType.VERB_1
            elif arity == 2:
                token_type = TokenType.VERB_2
            elif arity == 3:
                token_type = TokenType.VERB_3
            else:
                token_type = TokenType.VERB_VAR
            
            return Token(token_type, lexeme, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负甯冨皵瀛楅潰閲?        if lexeme in ('鐪?, '鍋?, 'true', 'false', 'True', 'False'):
            value = lexeme in ('鐪?, 'true', 'True')
            return Token(TokenType.BOOLEAN, value, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负绌哄€?        if lexeme == '绌?:
            return Token(TokenType.NULL, None, line_num, column, lexeme)
        
        # 灏濊瘯涓枃鍒嗚瘝
        if len(lexeme) > 1 and any('\u4e00' <= c <= '\u9fff' for c in lexeme):
            # 浣跨敤jieba杩涜涓枃鍒嗚瘝
            segments = self._segment(lexeme)
            if len(segments) > 1:
                # 濡傛灉鏄涓瘝锛岃繑鍥炵涓€涓瘝浣滀负鏍囪瘑绗?                first_segment = segments[0]
                # 閫掑綊澶勭悊绗竴涓瘝
                return self._parse_identifier(first_segment, 0, line_num, column)
        
        # 鏅€氭爣璇嗙
        return Token(TokenType.IDENTIFIER, lexeme, line_num, column, lexeme)
    
    def _is_identifier_char(self, char: str) -> bool:
        """妫€鏌ュ瓧绗︽槸鍚︿负鏍囪瘑绗﹀瓧绗?""
        # 涓枃瀛楃銆佽嫳鏂囧瓧姣嶃€佹暟瀛椼€佷笅鍒掔嚎
        return ('\u4e00' <= char <= '\u9fff' or
                'a' <= char <= 'z' or
                'A' <= char <= 'Z' or
                char.isdigit() or
                char == '_')
    
    def _get_keyword_type(self, lexeme: str) -> Optional[TokenType]:
        """鑾峰彇鍏抽敭璇嶇被鍨?""
        # 妫€鏌ョ姸鎬佸叧閿瘝锛堝瀛楋級
        for keyword, token_type in self.state_keywords.items():
            if lexeme.startswith(keyword):
                return token_type
        
        # 妫€鏌ユ劅鐭ュ叧閿瘝锛堝瀛楋級
        for keyword, token_type in self.perception_keywords.items():
            if lexeme.startswith(keyword):
                return token_type
        
        # 妫€鏌ユ椂闂村叧閿瘝锛堝瀛楋級
        for keyword, token_type in self.time_keywords.items():
            if lexeme.startswith(keyword):
                return token_type
        
        # 妫€鏌ユ櫘閫氬叧閿瘝
        return self.keywords.get(lexeme)
    
    def _is_bai_jia_xing(self, lexeme: str) -> bool:
        """妫€鏌ユ槸鍚︿负鐧惧濮撳彉閲?""
        if not lexeme:
            return False
        
        # 鑾峰彇濮撴皬锛堢涓€涓瓧绗︼級
        surname = lexeme[0]
        
        # 妫€鏌ユ槸鍚︿负鍐茬獊濮撴皬
        if surname in self.conflict_surnames:
            return False
        
        # 妫€鏌ユ槸鍚︿负鐧惧濮?        return surname in self.bai_jia_xing
    
    def print_tokens(self, tokens: List[Token]) -> None:
        """鎵撳嵃璇嶆硶鍗曞厓鍒楄〃"""
        print("璇嶆硶鍒嗘瀽缁撴灉:")
        print("=" * 80)
        print(f"{'琛?:<4} {'鍒?:<4} {'绫诲瀷':<20} {'鍊?:<20} {'璇嶇礌':<20}")
        print("-" * 80)
        
        for token in tokens:
            value_str = str(token.value)
            if len(value_str) > 18:
                value_str = value_str[:15] + "..."
            
            lexeme_str = token.lexeme
            if len(lexeme_str) > 18:
                lexeme_str = lexeme_str[:15] + "..."
            
            print(f"{token.line:<4} {token.column:<4} {token.type.value:<20} {value_str:<20} {lexeme_str:<20}")
        
        print("=" * 80)


# 娴嬭瘯鍑芥暟
def test_lexer():
    """娴嬭瘯璇嶆硶鍒嗘瀽鍣?""
    print("璇嶆硶鍒嗘瀽鍣ㄦ祴璇?)
    print("=" * 50)
    
    lexer = YanLuLexer()
    
    # 娴嬭瘯鐢ㄤ緥
    test_cases = [
        (
            "瀹氭俯搴︽槸25銆?,
            "鍙橀噺瀹氫箟"
        ),
        (
            "濡傛灉娓╁害澶?0灏卞紑鍚鎵囥€?,
            "鏉′欢璇彞"
        ),
        (
            "瀵逛簬i鍦?鍒?0锛氬嵃i銆?,
            "寰幆璇彞"
        ),
        (
            "娓╁害鍙樹负30搴︺€?,
            "鐘舵€佽浆鎹?
        ),
        (
            "寮犱笁銆佹潕鍥涳紝璁＄畻鎶樻墸銆?,
            "鎰忓悎寮忓嚱鏁拌皟鐢?
        ),
        (
            "'浣犲ソ锛屼笘鐣?",
            "瀛楃涓插瓧闈㈤噺"
        ),
        (
            "鐪熶笖鍋?,
            "甯冨皵杩愮畻"
        ),
        (
            "瀹歺绛変簬鍗佸姞浜斻€?,
            "涓枃鏁板瓧"
        ),
    ]
    
    for source_code, description in test_cases:
        print(f"\n娴嬭瘯: {description}")
        print(f"婧愪唬鐮? {source_code}")
        
        try:
            tokens = lexer.tokenize(source_code)
            lexer.print_tokens(tokens)
        except Exception as e:
            print(f"閿欒: {e}")
    
    print("=" * 50)
    print("娴嬭瘯瀹屾垚")


if __name__ == "__main__":
    test_lexer())
        self.identifier_pattern = re.compile(r'^[\u4e00-\u9fffA-Za-z_][\u4e00-\u9fffA-Za-z0-9_]*
        灏嗘簮浠ｇ爜杞崲涓鸿瘝娉曞崟鍏冨垪琛?        
        Args:
            source_code: 婧愪唬鐮佸瓧绗︿覆
            
        Returns:
            璇嶆硶鍗曞厓鍒楄〃
        """
        tokens = []
        lines = source_code.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            line_tokens = self._tokenize_line(line, line_num)
            tokens.extend(line_tokens)
            
            # 娣诲姞鎹㈣绗︼紙闄ら潪鏄渶鍚庝竴琛岋級
            if line_num < len(lines):
                tokens.append(Token(TokenType.NEWLINE, '\n', line_num, len(line) + 1, '\n'))
        
        # 娣诲姞鏂囦欢缁撴潫鏍囪
        tokens.append(Token(TokenType.EOF, '', len(lines) + 1, 1, ''))
        
        return tokens
    
    def _tokenize_line(self, line: str, line_num: int) -> List[Token]:
        """灏嗕竴琛屼唬鐮佽浆鎹负璇嶆硶鍗曞厓鍒楄〃"""
        tokens = []
        position = 0
        column = 1
        
        # 浣跨敤鍒嗚瘝鍣ㄨ繘琛屼腑鏂囧垎璇?        segments = self._segment(line)
        segment_index = 0
        
        while position < len(line):
            # 璺宠繃绌虹櫧瀛楃
            if line[position].isspace():
                if line[position] == '\n':
                    tokens.append(Token(TokenType.NEWLINE, '\n', line_num, column, '\n'))
                position += 1
                column += 1
                continue
            
            # 澶勭悊娉ㄩ噴
            if line[position] == '#':
                # 鍗曡娉ㄩ噴锛岃烦杩囨暣琛?                comment = line[position:]
                tokens.append(Token(TokenType.COMMENT, comment, line_num, column, comment))
                break
            
            # 澶勭悊澶氳瑷€浠ｇ爜鍧?            if line[position:position+2] == '{{':
                tokens.append(Token(TokenType.CODE_BLOCK_START, '{{', line_num, column, '{{'))
                position += 2
                column += 2
                continue
            
            if line[position:position+2] == '}}':
                tokens.append(Token(TokenType.CODE_BLOCK_END, '}}', line_num, column, '}}'))
                position += 2
                column += 2
                continue
            
            # 澶勭悊涓枃鏍囩偣绗﹀彿
            if line[position] in self.chinese_punctuation:
                char = line[position]
                token_type = self.chinese_punctuation[char]
                
                # 澶勭悊鎴愬鏍囩偣绗﹀彿
                if char in ('銆?, '銆?):
                    # 鏌ユ壘鍖归厤鐨勭粨鏉熺鍙?                    end_pos = line.find('銆? if char == '銆? else '銆?, position + 1)
                    if end_pos != -1:
                        value = line[position:end_pos + 1]
                        tokens.append(Token(token_type, value, line_num, column, value))
                        position = end_pos + 1
                        column += len(value)
                        continue
                
                tokens.append(Token(token_type, char, line_num, column, char))
                position += 1
                column += 1
                continue
            
            # 澶勭悊鐪佺暐鍙?            if line[position:position+2] == '鈥︹€?:
                tokens.append(Token(TokenType.ELLIPSIS, '鈥︹€?, line_num, column, '鈥︹€?))
                position += 2
                column += 2
                continue
            
            # 澶勭悊鐮存姌鍙?            if line[position:position+2] == '鈥斺€?:
                tokens.append(Token(TokenType.DASH, '鈥斺€?, line_num, column, '鈥斺€?))
                position += 2
                column += 2
                continue
            
            # 澶勭悊鍦嗗湀鍙?            if line[position] in '鈶犫憽鈶⑩懀鈶も懃鈶︹懅鈶ㄢ懇':
                tokens.append(Token(TokenType.CIRCLED_NUMBERS, line[position], line_num, column, line[position]))
                position += 1
                column += 1
                continue
            
            # 澶勭悊杩愮畻绗?            if line[position] in self.operators:
                # 妫€鏌ュ弻瀛楃杩愮畻绗?                if position + 1 < len(line):
                    two_char = line[position:position+2]
                    if two_char in ('鈮?, '鈮?, '鈮?):
                        tokens.append(Token(self.operators[two_char], two_char, line_num, column, two_char))
                        position += 2
                        column += 2
                        continue
                
                tokens.append(Token(self.operators[line[position]], line[position], line_num, column, line[position]))
                position += 1
                column += 1
                continue
            
            # 澶勭悊鍒嗙粍绗﹀彿
            if line[position] in self.grouping_symbols:
                tokens.append(Token(self.grouping_symbols[line[position]], line[position], line_num, column, line[position]))
                position += 1
                column += 1
                continue
            
            # 澶勭悊瀛楃涓插瓧闈㈤噺
            if line[position] in ('"', "'"):
                string_token = self._parse_string_literal(line, position, line_num, column)
                tokens.append(string_token)
                position += len(string_token.lexeme)
                column += len(string_token.lexeme)
                continue
            
            # 澶勭悊鏁板瓧瀛楅潰閲?            if line[position].isdigit() or (line[position] == '.' and position + 1 < len(line) and line[position + 1].isdigit()):
                number_token = self._parse_number(line, position, line_num, column)
                tokens.append(number_token)
                position += len(number_token.lexeme)
                column += len(number_token.lexeme)
                continue
            
            # 澶勭悊涓枃鏁板瓧
            if line[position] in self.chinese_numbers:
                chinese_number_token = self._parse_chinese_number(line, position, line_num, column)
                tokens.append(chinese_number_token)
                position += len(chinese_number_token.lexeme)
                column += len(chinese_number_token.lexeme)
                continue
            
            # 澶勭悊褰撳墠鍒嗚瘝娈?            if segment_index < len(segments):
                segment = segments[segment_index].strip()
                if segment:  # 璺宠繃绌哄垎璇?                    # 澶勭悊鍒嗚瘝娈?                    token = self._process_segment(segment, line_num, column)
                    tokens.append(token)
                    position += len(segment)
                    column += len(segment)
                segment_index += 1
            else:
                # 濡傛灉娌℃湁鏇村鍒嗚瘝锛屽鐞嗗墿浣欏瓧绗?                identifier_token = self._parse_identifier(line, position, line_num, column)
                tokens.append(identifier_token)
                position += len(identifier_token.lexeme)
                column += len(identifier_token.lexeme)
        
        return tokens
    
    def _process_segment(self, segment: str, line_num: int, column: int) -> Token:
        """澶勭悊鍒嗚瘝娈?""
        # 妫€鏌ユ槸鍚︿负鍏抽敭璇?        token_type = self._get_keyword_type(segment)
        if token_type:
            return Token(token_type, segment, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负鐧惧濮撳彉閲?        if self._is_bai_jia_xing(segment):
            return Token(TokenType.BAIJIAXING, segment, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负鍔ㄨ瘝
        arity = get_verb_arity(segment)
        if arity != 0:
            # 鏍规嵁鍏冩暟纭畾鍔ㄨ瘝绫诲瀷
            if arity == -1:
                token_type = TokenType.VERB_VAR
            elif arity == 0:
                token_type = TokenType.VERB_0
            elif arity == 1:
                token_type = TokenType.VERB_1
            elif arity == 2:
                token_type = TokenType.VERB_2
            elif arity == 3:
                token_type = TokenType.VERB_3
            else:
                token_type = TokenType.VERB_VAR
            
            return Token(token_type, segment, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负甯冨皵瀛楅潰閲?        if segment in ('鐪?, '鍋?, 'true', 'false', 'True', 'False'):
            value = segment in ('鐪?, 'true', 'True')
            return Token(TokenType.BOOLEAN, value, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负绌哄€?        if segment == '绌?:
            return Token(TokenType.NULL, None, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负鏁板瓧
        if segment.isdigit() or (segment.replace('.', '', 1).isdigit() and segment.count('.') == 1):
            try:
                if '.' in segment:
                    value = float(segment)
                else:
                    value = int(segment)
                return Token(TokenType.NUMBER, value, line_num, column, segment)
            except ValueError:
                pass
        
        # 妫€鏌ユ槸鍚︿负涓枃鏁板瓧
        if all(c in self.chinese_numbers for c in segment):
            value = self._chinese_to_arabic(segment)
            return Token(TokenType.CHINESE_NUMBER, value, line_num, column, segment)
        
        # 鏅€氭爣璇嗙
        return Token(TokenType.IDENTIFIER, segment, line_num, column, segment)
    
    def _parse_string_literal(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽瀛楃涓插瓧闈㈤噺"""
        quote_char = line[start]
        position = start + 1
        value = ''
        
        while position < len(line):
            char = line[position]
            
            if char == quote_char:
                # 缁撴潫寮曞彿
                position += 1
                break
            elif char == '\\' and position + 1 < len(line):
                # 杞箟瀛楃
                next_char = line[position + 1]
                if next_char in ('n', 't', '\\', '"', "'"):
                    value += self._escape_char(next_char)
                    position += 2
                else:
                    value += char
                    position += 1
            else:
                value += char
                position += 1
        
        lexeme = line[start:position]
        return Token(TokenType.STRING, value, line_num, column, lexeme)
    
    def _escape_char(self, char: str) -> str:
        """杞箟瀛楃"""
        escape_map = {
            'n': '\n',
            't': '\t',
            '\\': '\\',
            '"': '"',
            "'": "'",
        }
        return escape_map.get(char, char)
    
    def _parse_number(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽鏁板瓧瀛楅潰閲?""
        position = start
        
        # 瑙ｆ瀽鏁存暟閮ㄥ垎
        while position < len(line) and line[position].isdigit():
            position += 1
        
        # 瑙ｆ瀽灏忔暟閮ㄥ垎
        if position < len(line) and line[position] == '.':
            position += 1
            while position < len(line) and line[position].isdigit():
                position += 1
        
        # 瑙ｆ瀽绉戝璁℃暟娉?        if position < len(line) and line[position].lower() == 'e':
            position += 1
            if position < len(line) and line[position] in ('+', '-'):
                position += 1
            while position < len(line) and line[position].isdigit():
                position += 1
        
        lexeme = line[start:position]
        
        # 灏濊瘯杞崲涓烘暟瀛?        try:
            if '.' in lexeme or 'e' in lexeme.lower():
                value = float(lexeme)
            else:
                value = int(lexeme)
        except ValueError:
            value = lexeme  # 淇濇寔鍘熸牱
        
        return Token(TokenType.NUMBER, value, line_num, column, lexeme)
    
    def _parse_chinese_number(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽涓枃鏁板瓧"""
        position = start
        lexeme = ''
        
        while position < len(line) and line[position] in self.chinese_numbers:
            lexeme += line[position]
            position += 1
        
        # 杞崲涓洪樋鎷変集鏁板瓧
        value = self._chinese_to_arabic(lexeme)
        
        return Token(TokenType.CHINESE_NUMBER, value, line_num, column, lexeme)
    
    def _chinese_to_arabic(self, chinese_num: str) -> int:
        """灏嗕腑鏂囨暟瀛楄浆鎹负闃挎媺浼暟瀛?""
        if not chinese_num:
            return 0
        
        # 绠€鍗曞疄鐜帮紝鍙鐞嗗熀鏈暟瀛?        total = 0
        current = 0
        
        for char in chinese_num:
            num = self.chinese_numbers.get(char, 0)
            
            if num < 10:
                current = num
            elif num >= 10:
                if current == 0:
                    current = 1
                total += current * num
                current = 0
        
        total += current
        return total
    
    def _parse_identifier(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽鏍囪瘑绗?""
        position = start
        
        # 鏀堕泦鏍囪瘑绗﹀瓧绗?        while position < len(line) and self._is_identifier_char(line[position]):
            position += 1
        
        lexeme = line[start:position]
        
        # 妫€鏌ユ槸鍚︿负鍏抽敭璇?        token_type = self._get_keyword_type(lexeme)
        if token_type:
            return Token(token_type, lexeme, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负鐧惧濮撳彉閲?        if self._is_bai_jia_xing(lexeme):
            return Token(TokenType.BAIJIAXING, lexeme, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负鍔ㄨ瘝
        arity = get_verb_arity(lexeme)
        if arity != 0:
            # 鏍规嵁鍏冩暟纭畾鍔ㄨ瘝绫诲瀷
            if arity == -1:
                token_type = TokenType.VERB_VAR
            elif arity == 0:
                token_type = TokenType.VERB_0
            elif arity == 1:
                token_type = TokenType.VERB_1
            elif arity == 2:
                token_type = TokenType.VERB_2
            elif arity == 3:
                token_type = TokenType.VERB_3
            else:
                token_type = TokenType.VERB_VAR
            
            return Token(token_type, lexeme, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负甯冨皵瀛楅潰閲?        if lexeme in ('鐪?, '鍋?, 'true', 'false', 'True', 'False'):
            value = lexeme in ('鐪?, 'true', 'True')
            return Token(TokenType.BOOLEAN, value, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负绌哄€?        if lexeme == '绌?:
            return Token(TokenType.NULL, None, line_num, column, lexeme)
        
        # 灏濊瘯涓枃鍒嗚瘝
        if len(lexeme) > 1 and any('\u4e00' <= c <= '\u9fff' for c in lexeme):
            # 浣跨敤jieba杩涜涓枃鍒嗚瘝
            segments = self._segment(lexeme)
            if len(segments) > 1:
                # 濡傛灉鏄涓瘝锛岃繑鍥炵涓€涓瘝浣滀负鏍囪瘑绗?                first_segment = segments[0]
                # 閫掑綊澶勭悊绗竴涓瘝
                return self._parse_identifier(first_segment, 0, line_num, column)
        
        # 鏅€氭爣璇嗙
        return Token(TokenType.IDENTIFIER, lexeme, line_num, column, lexeme)
    
    def _is_identifier_char(self, char: str) -> bool:
        """妫€鏌ュ瓧绗︽槸鍚︿负鏍囪瘑绗﹀瓧绗?""
        # 涓枃瀛楃銆佽嫳鏂囧瓧姣嶃€佹暟瀛椼€佷笅鍒掔嚎
        return ('\u4e00' <= char <= '\u9fff' or
                'a' <= char <= 'z' or
                'A' <= char <= 'Z' or
                char.isdigit() or
                char == '_')
    
    def _get_keyword_type(self, lexeme: str) -> Optional[TokenType]:
        """鑾峰彇鍏抽敭璇嶇被鍨?""
        # 妫€鏌ョ姸鎬佸叧閿瘝锛堝瀛楋級
        for keyword, token_type in self.state_keywords.items():
            if lexeme.startswith(keyword):
                return token_type
        
        # 妫€鏌ユ劅鐭ュ叧閿瘝锛堝瀛楋級
        for keyword, token_type in self.perception_keywords.items():
            if lexeme.startswith(keyword):
                return token_type
        
        # 妫€鏌ユ椂闂村叧閿瘝锛堝瀛楋級
        for keyword, token_type in self.time_keywords.items():
            if lexeme.startswith(keyword):
                return token_type
        
        # 妫€鏌ユ櫘閫氬叧閿瘝
        return self.keywords.get(lexeme)
    
    def _is_bai_jia_xing(self, lexeme: str) -> bool:
        """妫€鏌ユ槸鍚︿负鐧惧濮撳彉閲?""
        if not lexeme:
            return False
        
        # 鑾峰彇濮撴皬锛堢涓€涓瓧绗︼級
        surname = lexeme[0]
        
        # 妫€鏌ユ槸鍚︿负鍐茬獊濮撴皬
        if surname in self.conflict_surnames:
            return False
        
        # 妫€鏌ユ槸鍚︿负鐧惧濮?        return surname in self.bai_jia_xing
    
    def print_tokens(self, tokens: List[Token]) -> None:
        """鎵撳嵃璇嶆硶鍗曞厓鍒楄〃"""
        print("璇嶆硶鍒嗘瀽缁撴灉:")
        print("=" * 80)
        print(f"{'琛?:<4} {'鍒?:<4} {'绫诲瀷':<20} {'鍊?:<20} {'璇嶇礌':<20}")
        print("-" * 80)
        
        for token in tokens:
            value_str = str(token.value)
            if len(value_str) > 18:
                value_str = value_str[:15] + "..."
            
            lexeme_str = token.lexeme
            if len(lexeme_str) > 18:
                lexeme_str = lexeme_str[:15] + "..."
            
            print(f"{token.line:<4} {token.column:<4} {token.type.value:<20} {value_str:<20} {lexeme_str:<20}")
        
        print("=" * 80)


# 娴嬭瘯鍑芥暟
def test_lexer():
    """娴嬭瘯璇嶆硶鍒嗘瀽鍣?""
    print("璇嶆硶鍒嗘瀽鍣ㄦ祴璇?)
    print("=" * 50)
    
    lexer = YanLuLexer()
    
    # 娴嬭瘯鐢ㄤ緥
    test_cases = [
        (
            "瀹氭俯搴︽槸25銆?,
            "鍙橀噺瀹氫箟"
        ),
        (
            "濡傛灉娓╁害澶?0灏卞紑鍚鎵囥€?,
            "鏉′欢璇彞"
        ),
        (
            "瀵逛簬i鍦?鍒?0锛氬嵃i銆?,
            "寰幆璇彞"
        ),
        (
            "娓╁害鍙樹负30搴︺€?,
            "鐘舵€佽浆鎹?
        ),
        (
            "寮犱笁銆佹潕鍥涳紝璁＄畻鎶樻墸銆?,
            "鎰忓悎寮忓嚱鏁拌皟鐢?
        ),
        (
            "'浣犲ソ锛屼笘鐣?",
            "瀛楃涓插瓧闈㈤噺"
        ),
        (
            "鐪熶笖鍋?,
            "甯冨皵杩愮畻"
        ),
        (
            "瀹歺绛変簬鍗佸姞浜斻€?,
            "涓枃鏁板瓧"
        ),
    ]
    
    for source_code, description in test_cases:
        print(f"\n娴嬭瘯: {description}")
        print(f"婧愪唬鐮? {source_code}")
        
        try:
            tokens = lexer.tokenize(source_code)
            lexer.print_tokens(tokens)
        except Exception as e:
            print(f"閿欒: {e}")
    
    print("=" * 50)
    print("娴嬭瘯瀹屾垚")


if __name__ == "__main__":
    test_lexer())
        self.identifier_pattern = re.compile(r'^[\u4e00-\u9fffA-Za-z_][\u4e00-\u9fffA-Za-z0-9_]*
        """
        灏嗘簮浠ｇ爜杞崲涓鸿瘝娉曞崟鍏冨垪琛?        
        Args:
            source_code: 婧愪唬鐮佸瓧绗︿覆
            
        Returns:
            璇嶆硶鍗曞厓鍒楄〃
        """
        tokens = []
        lines = source_code.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            line_tokens = self._tokenize_line(line, line_num)
            tokens.extend(line_tokens)
            
            # 娣诲姞鎹㈣绗︼紙闄ら潪鏄渶鍚庝竴琛岋級
            if line_num < len(lines):
                tokens.append(Token(TokenType.NEWLINE, '\n', line_num, len(line) + 1, '\n'))
        
        # 娣诲姞鏂囦欢缁撴潫鏍囪
        tokens.append(Token(TokenType.EOF, '', len(lines) + 1, 1, ''))
        
        return tokens
    
    def _tokenize_line(self, line: str, line_num: int) -> List[Token]:
        """灏嗕竴琛屼唬鐮佽浆鎹负璇嶆硶鍗曞厓鍒楄〃"""
        tokens = []
        position = 0
        column = 1
        
        # 浣跨敤鍒嗚瘝鍣ㄨ繘琛屼腑鏂囧垎璇?        segments = self._segment(line)
        segment_index = 0
        
        while position < len(line):
            # 璺宠繃绌虹櫧瀛楃
            if line[position].isspace():
                if line[position] == '\n':
                    tokens.append(Token(TokenType.NEWLINE, '\n', line_num, column, '\n'))
                position += 1
                column += 1
                continue
            
            # 澶勭悊娉ㄩ噴
            if line[position] == '#':
                # 鍗曡娉ㄩ噴锛岃烦杩囨暣琛?                comment = line[position:]
                tokens.append(Token(TokenType.COMMENT, comment, line_num, column, comment))
                break
            
            # 澶勭悊澶氳瑷€浠ｇ爜鍧?            if line[position:position+2] == '{{':
                tokens.append(Token(TokenType.CODE_BLOCK_START, '{{', line_num, column, '{{'))
                position += 2
                column += 2
                continue
            
            if line[position:position+2] == '}}':
                tokens.append(Token(TokenType.CODE_BLOCK_END, '}}', line_num, column, '}}'))
                position += 2
                column += 2
                continue
            
            # 澶勭悊涓枃鏍囩偣绗﹀彿
            if line[position] in self.chinese_punctuation:
                char = line[position]
                token_type = self.chinese_punctuation[char]
                
                # 澶勭悊鎴愬鏍囩偣绗﹀彿
                if char in ('銆?, '銆?):
                    # 鏌ユ壘鍖归厤鐨勭粨鏉熺鍙?                    end_pos = line.find('銆? if char == '銆? else '銆?, position + 1)
                    if end_pos != -1:
                        value = line[position:end_pos + 1]
                        tokens.append(Token(token_type, value, line_num, column, value))
                        position = end_pos + 1
                        column += len(value)
                        continue
                
                tokens.append(Token(token_type, char, line_num, column, char))
                position += 1
                column += 1
                continue
            
            # 澶勭悊鐪佺暐鍙?            if line[position:position+2] == '鈥︹€?:
                tokens.append(Token(TokenType.ELLIPSIS, '鈥︹€?, line_num, column, '鈥︹€?))
                position += 2
                column += 2
                continue
            
            # 澶勭悊鐮存姌鍙?            if line[position:position+2] == '鈥斺€?:
                tokens.append(Token(TokenType.DASH, '鈥斺€?, line_num, column, '鈥斺€?))
                position += 2
                column += 2
                continue
            
            # 澶勭悊鍦嗗湀鍙?            if line[position] in '鈶犫憽鈶⑩懀鈶も懃鈶︹懅鈶ㄢ懇':
                tokens.append(Token(TokenType.CIRCLED_NUMBERS, line[position], line_num, column, line[position]))
                position += 1
                column += 1
                continue
            
            # 澶勭悊杩愮畻绗?            if line[position] in self.operators:
                # 妫€鏌ュ弻瀛楃杩愮畻绗?                if position + 1 < len(line):
                    two_char = line[position:position+2]
                    if two_char in ('鈮?, '鈮?, '鈮?):
                        tokens.append(Token(self.operators[two_char], two_char, line_num, column, two_char))
                        position += 2
                        column += 2
                        continue
                
                tokens.append(Token(self.operators[line[position]], line[position], line_num, column, line[position]))
                position += 1
                column += 1
                continue
            
            # 澶勭悊鍒嗙粍绗﹀彿
            if line[position] in self.grouping_symbols:
                tokens.append(Token(self.grouping_symbols[line[position]], line[position], line_num, column, line[position]))
                position += 1
                column += 1
                continue
            
            # 澶勭悊瀛楃涓插瓧闈㈤噺
            if line[position] in ('"', "'"):
                string_token = self._parse_string_literal(line, position, line_num, column)
                tokens.append(string_token)
                position += len(string_token.lexeme)
                column += len(string_token.lexeme)
                continue
            
            # 澶勭悊鏁板瓧瀛楅潰閲?            if line[position].isdigit() or (line[position] == '.' and position + 1 < len(line) and line[position + 1].isdigit()):
                number_token = self._parse_number(line, position, line_num, column)
                tokens.append(number_token)
                position += len(number_token.lexeme)
                column += len(number_token.lexeme)
                continue
            
            # 澶勭悊涓枃鏁板瓧
            if line[position] in self.chinese_numbers:
                chinese_number_token = self._parse_chinese_number(line, position, line_num, column)
                tokens.append(chinese_number_token)
                position += len(chinese_number_token.lexeme)
                column += len(chinese_number_token.lexeme)
                continue
            
            # 澶勭悊褰撳墠鍒嗚瘝娈?            if segment_index < len(segments):
                segment = segments[segment_index].strip()
                if segment:  # 璺宠繃绌哄垎璇?                    # 澶勭悊鍒嗚瘝娈?                    token = self._process_segment(segment, line_num, column)
                    tokens.append(token)
                    position += len(segment)
                    column += len(segment)
                segment_index += 1
            else:
                # 濡傛灉娌℃湁鏇村鍒嗚瘝锛屽鐞嗗墿浣欏瓧绗?                identifier_token = self._parse_identifier(line, position, line_num, column)
                tokens.append(identifier_token)
                position += len(identifier_token.lexeme)
                column += len(identifier_token.lexeme)
        
        return tokens
    
    def _process_segment(self, segment: str, line_num: int, column: int) -> Token:
        """澶勭悊鍒嗚瘝娈?""
        # 妫€鏌ユ槸鍚︿负鍏抽敭璇?        token_type = self._get_keyword_type(segment)
        if token_type:
            return Token(token_type, segment, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负鐧惧濮撳彉閲?        if self._is_bai_jia_xing(segment):
            return Token(TokenType.BAIJIAXING, segment, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负鍔ㄨ瘝
        arity = get_verb_arity(segment)
        if arity != 0:
            # 鏍规嵁鍏冩暟纭畾鍔ㄨ瘝绫诲瀷
            if arity == -1:
                token_type = TokenType.VERB_VAR
            elif arity == 0:
                token_type = TokenType.VERB_0
            elif arity == 1:
                token_type = TokenType.VERB_1
            elif arity == 2:
                token_type = TokenType.VERB_2
            elif arity == 3:
                token_type = TokenType.VERB_3
            else:
                token_type = TokenType.VERB_VAR
            
            return Token(token_type, segment, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负甯冨皵瀛楅潰閲?        if segment in ('鐪?, '鍋?, 'true', 'false', 'True', 'False'):
            value = segment in ('鐪?, 'true', 'True')
            return Token(TokenType.BOOLEAN, value, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负绌哄€?        if segment == '绌?:
            return Token(TokenType.NULL, None, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负鏁板瓧
        if segment.isdigit() or (segment.replace('.', '', 1).isdigit() and segment.count('.') == 1):
            try:
                if '.' in segment:
                    value = float(segment)
                else:
                    value = int(segment)
                return Token(TokenType.NUMBER, value, line_num, column, segment)
            except ValueError:
                pass
        
        # 妫€鏌ユ槸鍚︿负涓枃鏁板瓧
        if all(c in self.chinese_numbers for c in segment):
            value = self._chinese_to_arabic(segment)
            return Token(TokenType.CHINESE_NUMBER, value, line_num, column, segment)
        
        # 鏅€氭爣璇嗙
        return Token(TokenType.IDENTIFIER, segment, line_num, column, segment)
    
    def _parse_string_literal(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽瀛楃涓插瓧闈㈤噺"""
        quote_char = line[start]
        position = start + 1
        value = ''
        
        while position < len(line):
            char = line[position]
            
            if char == quote_char:
                # 缁撴潫寮曞彿
                position += 1
                break
            elif char == '\\' and position + 1 < len(line):
                # 杞箟瀛楃
                next_char = line[position + 1]
                if next_char in ('n', 't', '\\', '"', "'"):
                    value += self._escape_char(next_char)
                    position += 2
                else:
                    value += char
                    position += 1
            else:
                value += char
                position += 1
        
        lexeme = line[start:position]
        return Token(TokenType.STRING, value, line_num, column, lexeme)
    
    def _escape_char(self, char: str) -> str:
        """杞箟瀛楃"""
        escape_map = {
            'n': '\n',
            't': '\t',
            '\\': '\\',
            '"': '"',
            "'": "'",
        }
        return escape_map.get(char, char)
    
    def _parse_number(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽鏁板瓧瀛楅潰閲?""
        position = start
        
        # 瑙ｆ瀽鏁存暟閮ㄥ垎
        while position < len(line) and line[position].isdigit():
            position += 1
        
        # 瑙ｆ瀽灏忔暟閮ㄥ垎
        if position < len(line) and line[position] == '.':
            position += 1
            while position < len(line) and line[position].isdigit():
                position += 1
        
        # 瑙ｆ瀽绉戝璁℃暟娉?        if position < len(line) and line[position].lower() == 'e':
            position += 1
            if position < len(line) and line[position] in ('+', '-'):
                position += 1
            while position < len(line) and line[position].isdigit():
                position += 1
        
        lexeme = line[start:position]
        
        # 灏濊瘯杞崲涓烘暟瀛?        try:
            if '.' in lexeme or 'e' in lexeme.lower():
                value = float(lexeme)
            else:
                value = int(lexeme)
        except ValueError:
            value = lexeme  # 淇濇寔鍘熸牱
        
        return Token(TokenType.NUMBER, value, line_num, column, lexeme)
    
    def _parse_chinese_number(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽涓枃鏁板瓧"""
        position = start
        lexeme = ''
        
        while position < len(line) and line[position] in self.chinese_numbers:
            lexeme += line[position]
            position += 1
        
        # 杞崲涓洪樋鎷変集鏁板瓧
        value = self._chinese_to_arabic(lexeme)
        
        return Token(TokenType.CHINESE_NUMBER, value, line_num, column, lexeme)
    
    def _chinese_to_arabic(self, chinese_num: str) -> int:
        """灏嗕腑鏂囨暟瀛楄浆鎹负闃挎媺浼暟瀛?""
        if not chinese_num:
            return 0
        
        # 绠€鍗曞疄鐜帮紝鍙鐞嗗熀鏈暟瀛?        total = 0
        current = 0
        
        for char in chinese_num:
            num = self.chinese_numbers.get(char, 0)
            
            if num < 10:
                current = num
            elif num >= 10:
                if current == 0:
                    current = 1
                total += current * num
                current = 0
        
        total += current
        return total
    
    def _parse_identifier(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽鏍囪瘑绗?""
        position = start
        
        # 鏀堕泦鏍囪瘑绗﹀瓧绗?        while position < len(line) and self._is_identifier_char(line[position]):
            position += 1
        
        lexeme = line[start:position]
        
        # 妫€鏌ユ槸鍚︿负鍏抽敭璇?        token_type = self._get_keyword_type(lexeme)
        if token_type:
            return Token(token_type, lexeme, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负鐧惧濮撳彉閲?        if self._is_bai_jia_xing(lexeme):
            return Token(TokenType.BAIJIAXING, lexeme, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负鍔ㄨ瘝
        arity = get_verb_arity(lexeme)
        if arity != 0:
            # 鏍规嵁鍏冩暟纭畾鍔ㄨ瘝绫诲瀷
            if arity == -1:
                token_type = TokenType.VERB_VAR
            elif arity == 0:
                token_type = TokenType.VERB_0
            elif arity == 1:
                token_type = TokenType.VERB_1
            elif arity == 2:
                token_type = TokenType.VERB_2
            elif arity == 3:
                token_type = TokenType.VERB_3
            else:
                token_type = TokenType.VERB_VAR
            
            return Token(token_type, lexeme, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负甯冨皵瀛楅潰閲?        if lexeme in ('鐪?, '鍋?, 'true', 'false', 'True', 'False'):
            value = lexeme in ('鐪?, 'true', 'True')
            return Token(TokenType.BOOLEAN, value, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负绌哄€?        if lexeme == '绌?:
            return Token(TokenType.NULL, None, line_num, column, lexeme)
        
        # 灏濊瘯涓枃鍒嗚瘝
        if len(lexeme) > 1 and any('\u4e00' <= c <= '\u9fff' for c in lexeme):
            # 浣跨敤jieba杩涜涓枃鍒嗚瘝
            segments = self._segment(lexeme)
            if len(segments) > 1:
                # 濡傛灉鏄涓瘝锛岃繑鍥炵涓€涓瘝浣滀负鏍囪瘑绗?                first_segment = segments[0]
                # 閫掑綊澶勭悊绗竴涓瘝
                return self._parse_identifier(first_segment, 0, line_num, column)
        
        # 鏅€氭爣璇嗙
        return Token(TokenType.IDENTIFIER, lexeme, line_num, column, lexeme)
    
    def _is_identifier_char(self, char: str) -> bool:
        """妫€鏌ュ瓧绗︽槸鍚︿负鏍囪瘑绗﹀瓧绗?""
        # 涓枃瀛楃銆佽嫳鏂囧瓧姣嶃€佹暟瀛椼€佷笅鍒掔嚎
        return ('\u4e00' <= char <= '\u9fff' or
                'a' <= char <= 'z' or
                'A' <= char <= 'Z' or
                char.isdigit() or
                char == '_')
    
    def _get_keyword_type(self, lexeme: str) -> Optional[TokenType]:
        """鑾峰彇鍏抽敭璇嶇被鍨?""
        # 妫€鏌ョ姸鎬佸叧閿瘝锛堝瀛楋級
        for keyword, token_type in self.state_keywords.items():
            if lexeme.startswith(keyword):
                return token_type
        
        # 妫€鏌ユ劅鐭ュ叧閿瘝锛堝瀛楋級
        for keyword, token_type in self.perception_keywords.items():
            if lexeme.startswith(keyword):
                return token_type
        
        # 妫€鏌ユ椂闂村叧閿瘝锛堝瀛楋級
        for keyword, token_type in self.time_keywords.items():
            if lexeme.startswith(keyword):
                return token_type
        
        # 妫€鏌ユ櫘閫氬叧閿瘝
        return self.keywords.get(lexeme)
    
    def _is_bai_jia_xing(self, lexeme: str) -> bool:
        """妫€鏌ユ槸鍚︿负鐧惧濮撳彉閲?""
        if not lexeme:
            return False
        
        # 鑾峰彇濮撴皬锛堢涓€涓瓧绗︼級
        surname = lexeme[0]
        
        # 妫€鏌ユ槸鍚︿负鍐茬獊濮撴皬
        if surname in self.conflict_surnames:
            return False
        
        # 妫€鏌ユ槸鍚︿负鐧惧濮?        return surname in self.bai_jia_xing
    
    def print_tokens(self, tokens: List[Token]) -> None:
        """鎵撳嵃璇嶆硶鍗曞厓鍒楄〃"""
        print("璇嶆硶鍒嗘瀽缁撴灉:")
        print("=" * 80)
        print(f"{'琛?:<4} {'鍒?:<4} {'绫诲瀷':<20} {'鍊?:<20} {'璇嶇礌':<20}")
        print("-" * 80)
        
        for token in tokens:
            value_str = str(token.value)
            if len(value_str) > 18:
                value_str = value_str[:15] + "..."
            
            lexeme_str = token.lexeme
            if len(lexeme_str) > 18:
                lexeme_str = lexeme_str[:15] + "..."
            
            print(f"{token.line:<4} {token.column:<4} {token.type.value:<20} {value_str:<20} {lexeme_str:<20}")
        
        print("=" * 80)


# 娴嬭瘯鍑芥暟
def test_lexer():
    """娴嬭瘯璇嶆硶鍒嗘瀽鍣?""
    print("璇嶆硶鍒嗘瀽鍣ㄦ祴璇?)
    print("=" * 50)
    
    lexer = YanLuLexer()
    
    # 娴嬭瘯鐢ㄤ緥
    test_cases = [
        (
            "瀹氭俯搴︽槸25銆?,
            "鍙橀噺瀹氫箟"
        ),
        (
            "濡傛灉娓╁害澶?0灏卞紑鍚鎵囥€?,
            "鏉′欢璇彞"
        ),
        (
            "瀵逛簬i鍦?鍒?0锛氬嵃i銆?,
            "寰幆璇彞"
        ),
        (
            "娓╁害鍙樹负30搴︺€?,
            "鐘舵€佽浆鎹?
        ),
        (
            "寮犱笁銆佹潕鍥涳紝璁＄畻鎶樻墸銆?,
            "鎰忓悎寮忓嚱鏁拌皟鐢?
        ),
        (
            "'浣犲ソ锛屼笘鐣?",
            "瀛楃涓插瓧闈㈤噺"
        ),
        (
            "鐪熶笖鍋?,
            "甯冨皵杩愮畻"
        ),
        (
            "瀹歺绛変簬鍗佸姞浜斻€?,
            "涓枃鏁板瓧"
        ),
    ]
    
    for source_code, description in test_cases:
        print(f"\n娴嬭瘯: {description}")
        print(f"婧愪唬鐮? {source_code}")
        
        try:
            tokens = lexer.tokenize(source_code)
            lexer.print_tokens(tokens)
        except Exception as e:
            print(f"閿欒: {e}")
    
    print("=" * 50)
    print("娴嬭瘯瀹屾垚")


if __name__ == "__main__":
    test_lexer())
    
    def _init_segmenter(self):
        """鍒濆鍖栧垎璇嶅櫒"""
        if self.segmenter_type == "thulac":
            try:
                import thulac
                # 浣跨敤seg_only=True鍙繘琛屽垎璇嶏紝涓嶈繘琛岃瘝鎬ф爣娉?                self.segmenter = thulac.thulac(seg_only=True, model_path=None)
                print(f"浣跨敤THULAC鍒嗚瘝鍣?(seg_only妯″紡)")
            except ImportError:
                print("璀﹀憡: 鏈畨瑁匱HULAC锛屽洖閫€鍒癹ieba鍒嗚瘝鍣?)
                print("瀹夎鍛戒护: pip install thulac")
                self.segmenter_type = "jieba"
                self.segmenter = jieba
        else:
            # 榛樿浣跨敤jieba
            self.segmenter = jieba
            print(f"浣跨敤jieba鍒嗚瘝鍣?)
    
    def _segment(self, text: str) -> List[str]:
        """
        鍒嗚瘝鏂规硶
        
        Args:
            text: 寰呭垎璇嶇殑鏂囨湰
            
        Returns:
            鍒嗚瘝缁撴灉鍒楄〃
        """
        if self.segmenter_type == "thulac":
            # THULAC鍒嗚瘝
            result = self.segmenter.cut(text, text=True)
            return result.split()
        else:
            # jieba鍒嗚瘝
            return list(self.segmenter.lcut(text))
        
    def tokenize(self, source_code: str) -> List[Token]:
        """
        灏嗘簮浠ｇ爜杞崲涓鸿瘝娉曞崟鍏冨垪琛?        
        Args:
            source_code: 婧愪唬鐮佸瓧绗︿覆
            
        Returns:
            璇嶆硶鍗曞厓鍒楄〃
        """
        tokens = []
        lines = source_code.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            line_tokens = self._tokenize_line(line, line_num)
            tokens.extend(line_tokens)
            
            # 娣诲姞鎹㈣绗︼紙闄ら潪鏄渶鍚庝竴琛岋級
            if line_num < len(lines):
                tokens.append(Token(TokenType.NEWLINE, '\n', line_num, len(line) + 1, '\n'))
        
        # 娣诲姞鏂囦欢缁撴潫鏍囪
        tokens.append(Token(TokenType.EOF, '', len(lines) + 1, 1, ''))
        
        return tokens
    
    def _tokenize_line(self, line: str, line_num: int) -> List[Token]:
        """灏嗕竴琛屼唬鐮佽浆鎹负璇嶆硶鍗曞厓鍒楄〃"""
        tokens = []
        position = 0
        column = 1
        
        # 浣跨敤鍒嗚瘝鍣ㄨ繘琛屼腑鏂囧垎璇?        segments = self._segment(line)
        segment_index = 0
        
        while position < len(line):
            # 璺宠繃绌虹櫧瀛楃
            if line[position].isspace():
                if line[position] == '\n':
                    tokens.append(Token(TokenType.NEWLINE, '\n', line_num, column, '\n'))
                position += 1
                column += 1
                continue
            
            # 澶勭悊娉ㄩ噴
            if line[position] == '#':
                # 鍗曡娉ㄩ噴锛岃烦杩囨暣琛?                comment = line[position:]
                tokens.append(Token(TokenType.COMMENT, comment, line_num, column, comment))
                break
            
            # 澶勭悊澶氳瑷€浠ｇ爜鍧?            if line[position:position+2] == '{{':
                tokens.append(Token(TokenType.CODE_BLOCK_START, '{{', line_num, column, '{{'))
                position += 2
                column += 2
                continue
            
            if line[position:position+2] == '}}':
                tokens.append(Token(TokenType.CODE_BLOCK_END, '}}', line_num, column, '}}'))
                position += 2
                column += 2
                continue
            
            # 澶勭悊涓枃鏍囩偣绗﹀彿
            if line[position] in self.chinese_punctuation:
                char = line[position]
                token_type = self.chinese_punctuation[char]
                
                # 澶勭悊鎴愬鏍囩偣绗﹀彿
                if char in ('銆?, '銆?):
                    # 鏌ユ壘鍖归厤鐨勭粨鏉熺鍙?                    end_pos = line.find('銆? if char == '銆? else '銆?, position + 1)
                    if end_pos != -1:
                        value = line[position:end_pos + 1]
                        tokens.append(Token(token_type, value, line_num, column, value))
                        position = end_pos + 1
                        column += len(value)
                        continue
                
                tokens.append(Token(token_type, char, line_num, column, char))
                position += 1
                column += 1
                continue
            
            # 澶勭悊鐪佺暐鍙?            if line[position:position+2] == '鈥︹€?:
                tokens.append(Token(TokenType.ELLIPSIS, '鈥︹€?, line_num, column, '鈥︹€?))
                position += 2
                column += 2
                continue
            
            # 澶勭悊鐮存姌鍙?            if line[position:position+2] == '鈥斺€?:
                tokens.append(Token(TokenType.DASH, '鈥斺€?, line_num, column, '鈥斺€?))
                position += 2
                column += 2
                continue
            
            # 澶勭悊鍦嗗湀鍙?            if line[position] in '鈶犫憽鈶⑩懀鈶も懃鈶︹懅鈶ㄢ懇':
                tokens.append(Token(TokenType.CIRCLED_NUMBERS, line[position], line_num, column, line[position]))
                position += 1
                column += 1
                continue
            
            # 澶勭悊杩愮畻绗?            if line[position] in self.operators:
                # 妫€鏌ュ弻瀛楃杩愮畻绗?                if position + 1 < len(line):
                    two_char = line[position:position+2]
                    if two_char in ('鈮?, '鈮?, '鈮?):
                        tokens.append(Token(self.operators[two_char], two_char, line_num, column, two_char))
                        position += 2
                        column += 2
                        continue
                
                tokens.append(Token(self.operators[line[position]], line[position], line_num, column, line[position]))
                position += 1
                column += 1
                continue
            
            # 澶勭悊鍒嗙粍绗﹀彿
            if line[position] in self.grouping_symbols:
                tokens.append(Token(self.grouping_symbols[line[position]], line[position], line_num, column, line[position]))
                position += 1
                column += 1
                continue
            
            # 澶勭悊瀛楃涓插瓧闈㈤噺
            if line[position] in ('"', "'"):
                string_token = self._parse_string_literal(line, position, line_num, column)
                tokens.append(string_token)
                position += len(string_token.lexeme)
                column += len(string_token.lexeme)
                continue
            
            # 澶勭悊鏁板瓧瀛楅潰閲?            if line[position].isdigit() or (line[position] == '.' and position + 1 < len(line) and line[position + 1].isdigit()):
                number_token = self._parse_number(line, position, line_num, column)
                tokens.append(number_token)
                position += len(number_token.lexeme)
                column += len(number_token.lexeme)
                continue
            
            # 澶勭悊涓枃鏁板瓧
            if line[position] in self.chinese_numbers:
                chinese_number_token = self._parse_chinese_number(line, position, line_num, column)
                tokens.append(chinese_number_token)
                position += len(chinese_number_token.lexeme)
                column += len(chinese_number_token.lexeme)
                continue
            
            # 澶勭悊褰撳墠鍒嗚瘝娈?            if segment_index < len(segments):
                segment = segments[segment_index].strip()
                if segment:  # 璺宠繃绌哄垎璇?                    # 澶勭悊鍒嗚瘝娈?                    token = self._process_segment(segment, line_num, column)
                    tokens.append(token)
                    position += len(segment)
                    column += len(segment)
                segment_index += 1
            else:
                # 濡傛灉娌℃湁鏇村鍒嗚瘝锛屽鐞嗗墿浣欏瓧绗?                identifier_token = self._parse_identifier(line, position, line_num, column)
                tokens.append(identifier_token)
                position += len(identifier_token.lexeme)
                column += len(identifier_token.lexeme)
        
        return tokens
    
    def _process_segment(self, segment: str, line_num: int, column: int) -> Token:
        """澶勭悊鍒嗚瘝娈?""
        # 妫€鏌ユ槸鍚︿负鍏抽敭璇?        token_type = self._get_keyword_type(segment)
        if token_type:
            return Token(token_type, segment, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负鐧惧濮撳彉閲?        if self._is_bai_jia_xing(segment):
            return Token(TokenType.BAIJIAXING, segment, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负鍔ㄨ瘝
        arity = get_verb_arity(segment)
        if arity != 0:
            # 鏍规嵁鍏冩暟纭畾鍔ㄨ瘝绫诲瀷
            if arity == -1:
                token_type = TokenType.VERB_VAR
            elif arity == 0:
                token_type = TokenType.VERB_0
            elif arity == 1:
                token_type = TokenType.VERB_1
            elif arity == 2:
                token_type = TokenType.VERB_2
            elif arity == 3:
                token_type = TokenType.VERB_3
            else:
                token_type = TokenType.VERB_VAR
            
            return Token(token_type, segment, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负甯冨皵瀛楅潰閲?        if segment in ('鐪?, '鍋?, 'true', 'false', 'True', 'False'):
            value = segment in ('鐪?, 'true', 'True')
            return Token(TokenType.BOOLEAN, value, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负绌哄€?        if segment == '绌?:
            return Token(TokenType.NULL, None, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负鏁板瓧
        if segment.isdigit() or (segment.replace('.', '', 1).isdigit() and segment.count('.') == 1):
            try:
                if '.' in segment:
                    value = float(segment)
                else:
                    value = int(segment)
                return Token(TokenType.NUMBER, value, line_num, column, segment)
            except ValueError:
                pass
        
        # 妫€鏌ユ槸鍚︿负涓枃鏁板瓧
        if all(c in self.chinese_numbers for c in segment):
            value = self._chinese_to_arabic(segment)
            return Token(TokenType.CHINESE_NUMBER, value, line_num, column, segment)
        
        # 鏅€氭爣璇嗙
        return Token(TokenType.IDENTIFIER, segment, line_num, column, segment)
    
    def _parse_string_literal(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽瀛楃涓插瓧闈㈤噺"""
        quote_char = line[start]
        position = start + 1
        value = ''
        
        while position < len(line):
            char = line[position]
            
            if char == quote_char:
                # 缁撴潫寮曞彿
                position += 1
                break
            elif char == '\\' and position + 1 < len(line):
                # 杞箟瀛楃
                next_char = line[position + 1]
                if next_char in ('n', 't', '\\', '"', "'"):
                    value += self._escape_char(next_char)
                    position += 2
                else:
                    value += char
                    position += 1
            else:
                value += char
                position += 1
        
        lexeme = line[start:position]
        return Token(TokenType.STRING, value, line_num, column, lexeme)
    
    def _escape_char(self, char: str) -> str:
        """杞箟瀛楃"""
        escape_map = {
            'n': '\n',
            't': '\t',
            '\\': '\\',
            '"': '"',
            "'": "'",
        }
        return escape_map.get(char, char)
    
    def _parse_number(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽鏁板瓧瀛楅潰閲?""
        position = start
        
        # 瑙ｆ瀽鏁存暟閮ㄥ垎
        while position < len(line) and line[position].isdigit():
            position += 1
        
        # 瑙ｆ瀽灏忔暟閮ㄥ垎
        if position < len(line) and line[position] == '.':
            position += 1
            while position < len(line) and line[position].isdigit():
                position += 1
        
        # 瑙ｆ瀽绉戝璁℃暟娉?        if position < len(line) and line[position].lower() == 'e':
            position += 1
            if position < len(line) and line[position] in ('+', '-'):
                position += 1
            while position < len(line) and line[position].isdigit():
                position += 1
        
        lexeme = line[start:position]
        
        # 灏濊瘯杞崲涓烘暟瀛?        try:
            if '.' in lexeme or 'e' in lexeme.lower():
                value = float(lexeme)
            else:
                value = int(lexeme)
        except ValueError:
            value = lexeme  # 淇濇寔鍘熸牱
        
        return Token(TokenType.NUMBER, value, line_num, column, lexeme)
    
    def _parse_chinese_number(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽涓枃鏁板瓧"""
        position = start
        lexeme = ''
        
        while position < len(line) and line[position] in self.chinese_numbers:
            lexeme += line[position]
            position += 1
        
        # 杞崲涓洪樋鎷変集鏁板瓧
        value = self._chinese_to_arabic(lexeme)
        
        return Token(TokenType.CHINESE_NUMBER, value, line_num, column, lexeme)
    
    def _chinese_to_arabic(self, chinese_num: str) -> int:
        """灏嗕腑鏂囨暟瀛楄浆鎹负闃挎媺浼暟瀛?""
        if not chinese_num:
            return 0
        
        # 绠€鍗曞疄鐜帮紝鍙鐞嗗熀鏈暟瀛?        total = 0
        current = 0
        
        for char in chinese_num:
            num = self.chinese_numbers.get(char, 0)
            
            if num < 10:
                current = num
            elif num >= 10:
                if current == 0:
                    current = 1
                total += current * num
                current = 0
        
        total += current
        return total
    
    def _parse_identifier(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽鏍囪瘑绗?""
        position = start
        
        # 鏀堕泦鏍囪瘑绗﹀瓧绗?        while position < len(line) and self._is_identifier_char(line[position]):
            position += 1
        
        lexeme = line[start:position]
        
        # 妫€鏌ユ槸鍚︿负鍏抽敭璇?        token_type = self._get_keyword_type(lexeme)
        if token_type:
            return Token(token_type, lexeme, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负鐧惧濮撳彉閲?        if self._is_bai_jia_xing(lexeme):
            return Token(TokenType.BAIJIAXING, lexeme, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负鍔ㄨ瘝
        arity = get_verb_arity(lexeme)
        if arity != 0:
            # 鏍规嵁鍏冩暟纭畾鍔ㄨ瘝绫诲瀷
            if arity == -1:
                token_type = TokenType.VERB_VAR
            elif arity == 0:
                token_type = TokenType.VERB_0
            elif arity == 1:
                token_type = TokenType.VERB_1
            elif arity == 2:
                token_type = TokenType.VERB_2
            elif arity == 3:
                token_type = TokenType.VERB_3
            else:
                token_type = TokenType.VERB_VAR
            
            return Token(token_type, lexeme, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负甯冨皵瀛楅潰閲?        if lexeme in ('鐪?, '鍋?, 'true', 'false', 'True', 'False'):
            value = lexeme in ('鐪?, 'true', 'True')
            return Token(TokenType.BOOLEAN, value, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负绌哄€?        if lexeme == '绌?:
            return Token(TokenType.NULL, None, line_num, column, lexeme)
        
        # 灏濊瘯涓枃鍒嗚瘝
        if len(lexeme) > 1 and any('\u4e00' <= c <= '\u9fff' for c in lexeme):
            # 浣跨敤jieba杩涜涓枃鍒嗚瘝
            segments = self._segment(lexeme)
            if len(segments) > 1:
                # 濡傛灉鏄涓瘝锛岃繑鍥炵涓€涓瘝浣滀负鏍囪瘑绗?                first_segment = segments[0]
                # 閫掑綊澶勭悊绗竴涓瘝
                return self._parse_identifier(first_segment, 0, line_num, column)
        
        # 鏅€氭爣璇嗙
        return Token(TokenType.IDENTIFIER, lexeme, line_num, column, lexeme)
    
    def _is_identifier_char(self, char: str) -> bool:
        """妫€鏌ュ瓧绗︽槸鍚︿负鏍囪瘑绗﹀瓧绗?""
        # 涓枃瀛楃銆佽嫳鏂囧瓧姣嶃€佹暟瀛椼€佷笅鍒掔嚎
        return ('\u4e00' <= char <= '\u9fff' or
                'a' <= char <= 'z' or
                'A' <= char <= 'Z' or
                char.isdigit() or
                char == '_')
    
    def _get_keyword_type(self, lexeme: str) -> Optional[TokenType]:
        """鑾峰彇鍏抽敭璇嶇被鍨?""
        # 妫€鏌ョ姸鎬佸叧閿瘝锛堝瀛楋級
        for keyword, token_type in self.state_keywords.items():
            if lexeme.startswith(keyword):
                return token_type
        
        # 妫€鏌ユ劅鐭ュ叧閿瘝锛堝瀛楋級
        for keyword, token_type in self.perception_keywords.items():
            if lexeme.startswith(keyword):
                return token_type
        
        # 妫€鏌ユ椂闂村叧閿瘝锛堝瀛楋級
        for keyword, token_type in self.time_keywords.items():
            if lexeme.startswith(keyword):
                return token_type
        
        # 妫€鏌ユ櫘閫氬叧閿瘝
        return self.keywords.get(lexeme)
    
    def _is_bai_jia_xing(self, lexeme: str) -> bool:
        """妫€鏌ユ槸鍚︿负鐧惧濮撳彉閲?""
        if not lexeme:
            return False
        
        # 鑾峰彇濮撴皬锛堢涓€涓瓧绗︼級
        surname = lexeme[0]
        
        # 妫€鏌ユ槸鍚︿负鍐茬獊濮撴皬
        if surname in self.conflict_surnames:
            return False
        
        # 妫€鏌ユ槸鍚︿负鐧惧濮?        return surname in self.bai_jia_xing
    
    def print_tokens(self, tokens: List[Token]) -> None:
        """鎵撳嵃璇嶆硶鍗曞厓鍒楄〃"""
        print("璇嶆硶鍒嗘瀽缁撴灉:")
        print("=" * 80)
        print(f"{'琛?:<4} {'鍒?:<4} {'绫诲瀷':<20} {'鍊?:<20} {'璇嶇礌':<20}")
        print("-" * 80)
        
        for token in tokens:
            value_str = str(token.value)
            if len(value_str) > 18:
                value_str = value_str[:15] + "..."
            
            lexeme_str = token.lexeme
            if len(lexeme_str) > 18:
                lexeme_str = lexeme_str[:15] + "..."
            
            print(f"{token.line:<4} {token.column:<4} {token.type.value:<20} {value_str:<20} {lexeme_str:<20}")
        
        print("=" * 80)


# 娴嬭瘯鍑芥暟
def test_lexer():
    """娴嬭瘯璇嶆硶鍒嗘瀽鍣?""
    print("璇嶆硶鍒嗘瀽鍣ㄦ祴璇?)
    print("=" * 50)
    
    lexer = YanLuLexer()
    
    # 娴嬭瘯鐢ㄤ緥
    test_cases = [
        (
            "瀹氭俯搴︽槸25銆?,
            "鍙橀噺瀹氫箟"
        ),
        (
            "濡傛灉娓╁害澶?0灏卞紑鍚鎵囥€?,
            "鏉′欢璇彞"
        ),
        (
            "瀵逛簬i鍦?鍒?0锛氬嵃i銆?,
            "寰幆璇彞"
        ),
        (
            "娓╁害鍙樹负30搴︺€?,
            "鐘舵€佽浆鎹?
        ),
        (
            "寮犱笁銆佹潕鍥涳紝璁＄畻鎶樻墸銆?,
            "鎰忓悎寮忓嚱鏁拌皟鐢?
        ),
        (
            "'浣犲ソ锛屼笘鐣?",
            "瀛楃涓插瓧闈㈤噺"
        ),
        (
            "鐪熶笖鍋?,
            "甯冨皵杩愮畻"
        ),
        (
            "瀹歺绛変簬鍗佸姞浜斻€?,
            "涓枃鏁板瓧"
        ),
    ]
    
    for source_code, description in test_cases:
        print(f"\n娴嬭瘯: {description}")
        print(f"婧愪唬鐮? {source_code}")
        
        try:
            tokens = lexer.tokenize(source_code)
            lexer.print_tokens(tokens)
        except Exception as e:
            print(f"閿欒: {e}")
    
    print("=" * 50)
    print("娴嬭瘯瀹屾垚")


if __name__ == "__main__":
    test_lexer())
    
    def _init_segmenter(self):
        """鍒濆鍖栧垎璇嶅櫒"""
        if self.segmenter_type == "thulac":
            try:
                import thulac
                # 浣跨敤seg_only=True鍙繘琛屽垎璇嶏紝涓嶈繘琛岃瘝鎬ф爣娉?                self.segmenter = thulac.thulac(seg_only=True, model_path=None)
                print(f"浣跨敤THULAC鍒嗚瘝鍣?(seg_only妯″紡)")
            except ImportError:
                print("璀﹀憡: 鏈畨瑁匱HULAC锛屽洖閫€鍒癹ieba鍒嗚瘝鍣?)
                print("瀹夎鍛戒护: pip install thulac")
                self.segmenter_type = "jieba"
                self.segmenter = jieba
        else:
            # 榛樿浣跨敤jieba
            self.segmenter = jieba
            print(f"浣跨敤jieba鍒嗚瘝鍣?)
    
    def _segment(self, text: str) -> List[str]:
        """
        鍒嗚瘝鏂规硶
        
        Args:
            text: 寰呭垎璇嶇殑鏂囨湰
            
        Returns:
            鍒嗚瘝缁撴灉鍒楄〃
        """
        if self.segmenter_type == "thulac":
            # THULAC鍒嗚瘝
            result = self.segmenter.cut(text, text=True)
            return result.split()
        else:
            # jieba鍒嗚瘝
            return list(self.segmenter.lcut(text))
        
    def tokenize(self, source_code: str) -> List[Token]:
        """
        灏嗘簮浠ｇ爜杞崲涓鸿瘝娉曞崟鍏冨垪琛?        
        Args:
            source_code: 婧愪唬鐮佸瓧绗︿覆
            
        Returns:
            璇嶆硶鍗曞厓鍒楄〃
        """
        tokens = []
        lines = source_code.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            line_tokens = self._tokenize_line(line, line_num)
            tokens.extend(line_tokens)
            
            # 娣诲姞鎹㈣绗︼紙闄ら潪鏄渶鍚庝竴琛岋級
            if line_num < len(lines):
                tokens.append(Token(TokenType.NEWLINE, '\n', line_num, len(line) + 1, '\n'))
        
        # 娣诲姞鏂囦欢缁撴潫鏍囪
        tokens.append(Token(TokenType.EOF, '', len(lines) + 1, 1, ''))
        
        return tokens
    
    def _tokenize_line(self, line: str, line_num: int) -> List[Token]:
        """灏嗕竴琛屼唬鐮佽浆鎹负璇嶆硶鍗曞厓鍒楄〃"""
        tokens = []
        position = 0
        column = 1
        
        # 浣跨敤鍒嗚瘝鍣ㄨ繘琛屼腑鏂囧垎璇?        segments = self._segment(line)
        segment_index = 0
        
        while position < len(line):
            # 璺宠繃绌虹櫧瀛楃
            if line[position].isspace():
                if line[position] == '\n':
                    tokens.append(Token(TokenType.NEWLINE, '\n', line_num, column, '\n'))
                position += 1
                column += 1
                continue
            
            # 澶勭悊娉ㄩ噴
            if line[position] == '#':
                # 鍗曡娉ㄩ噴锛岃烦杩囨暣琛?                comment = line[position:]
                tokens.append(Token(TokenType.COMMENT, comment, line_num, column, comment))
                break
            
            # 澶勭悊澶氳瑷€浠ｇ爜鍧?            if line[position:position+2] == '{{':
                tokens.append(Token(TokenType.CODE_BLOCK_START, '{{', line_num, column, '{{'))
                position += 2
                column += 2
                continue
            
            if line[position:position+2] == '}}':
                tokens.append(Token(TokenType.CODE_BLOCK_END, '}}', line_num, column, '}}'))
                position += 2
                column += 2
                continue
            
            # 澶勭悊涓枃鏍囩偣绗﹀彿
            if line[position] in self.chinese_punctuation:
                char = line[position]
                token_type = self.chinese_punctuation[char]
                
                # 澶勭悊鎴愬鏍囩偣绗﹀彿
                if char in ('銆?, '銆?):
                    # 鏌ユ壘鍖归厤鐨勭粨鏉熺鍙?                    end_pos = line.find('銆? if char == '銆? else '銆?, position + 1)
                    if end_pos != -1:
                        value = line[position:end_pos + 1]
                        tokens.append(Token(token_type, value, line_num, column, value))
                        position = end_pos + 1
                        column += len(value)
                        continue
                
                tokens.append(Token(token_type, char, line_num, column, char))
                position += 1
                column += 1
                continue
            
            # 澶勭悊鐪佺暐鍙?            if line[position:position+2] == '鈥︹€?:
                tokens.append(Token(TokenType.ELLIPSIS, '鈥︹€?, line_num, column, '鈥︹€?))
                position += 2
                column += 2
                continue
            
            # 澶勭悊鐮存姌鍙?            if line[position:position+2] == '鈥斺€?:
                tokens.append(Token(TokenType.DASH, '鈥斺€?, line_num, column, '鈥斺€?))
                position += 2
                column += 2
                continue
            
            # 澶勭悊鍦嗗湀鍙?            if line[position] in '鈶犫憽鈶⑩懀鈶も懃鈶︹懅鈶ㄢ懇':
                tokens.append(Token(TokenType.CIRCLED_NUMBERS, line[position], line_num, column, line[position]))
                position += 1
                column += 1
                continue
            
            # 澶勭悊杩愮畻绗?            if line[position] in self.operators:
                # 妫€鏌ュ弻瀛楃杩愮畻绗?                if position + 1 < len(line):
                    two_char = line[position:position+2]
                    if two_char in ('鈮?, '鈮?, '鈮?):
                        tokens.append(Token(self.operators[two_char], two_char, line_num, column, two_char))
                        position += 2
                        column += 2
                        continue
                
                tokens.append(Token(self.operators[line[position]], line[position], line_num, column, line[position]))
                position += 1
                column += 1
                continue
            
            # 澶勭悊鍒嗙粍绗﹀彿
            if line[position] in self.grouping_symbols:
                tokens.append(Token(self.grouping_symbols[line[position]], line[position], line_num, column, line[position]))
                position += 1
                column += 1
                continue
            
            # 澶勭悊瀛楃涓插瓧闈㈤噺
            if line[position] in ('"', "'"):
                string_token = self._parse_string_literal(line, position, line_num, column)
                tokens.append(string_token)
                position += len(string_token.lexeme)
                column += len(string_token.lexeme)
                continue
            
            # 澶勭悊鏁板瓧瀛楅潰閲?            if line[position].isdigit() or (line[position] == '.' and position + 1 < len(line) and line[position + 1].isdigit()):
                number_token = self._parse_number(line, position, line_num, column)
                tokens.append(number_token)
                position += len(number_token.lexeme)
                column += len(number_token.lexeme)
                continue
            
            # 澶勭悊涓枃鏁板瓧
            if line[position] in self.chinese_numbers:
                chinese_number_token = self._parse_chinese_number(line, position, line_num, column)
                tokens.append(chinese_number_token)
                position += len(chinese_number_token.lexeme)
                column += len(chinese_number_token.lexeme)
                continue
            
            # 澶勭悊褰撳墠鍒嗚瘝娈?            if segment_index < len(segments):
                segment = segments[segment_index].strip()
                if segment:  # 璺宠繃绌哄垎璇?                    # 澶勭悊鍒嗚瘝娈?                    token = self._process_segment(segment, line_num, column)
                    tokens.append(token)
                    position += len(segment)
                    column += len(segment)
                segment_index += 1
            else:
                # 濡傛灉娌℃湁鏇村鍒嗚瘝锛屽鐞嗗墿浣欏瓧绗?                identifier_token = self._parse_identifier(line, position, line_num, column)
                tokens.append(identifier_token)
                position += len(identifier_token.lexeme)
                column += len(identifier_token.lexeme)
        
        return tokens
    
    def _process_segment(self, segment: str, line_num: int, column: int) -> Token:
        """澶勭悊鍒嗚瘝娈?""
        # 妫€鏌ユ槸鍚︿负鍏抽敭璇?        token_type = self._get_keyword_type(segment)
        if token_type:
            return Token(token_type, segment, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负鐧惧濮撳彉閲?        if self._is_bai_jia_xing(segment):
            return Token(TokenType.BAIJIAXING, segment, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负鍔ㄨ瘝
        arity = get_verb_arity(segment)
        if arity != 0:
            # 鏍规嵁鍏冩暟纭畾鍔ㄨ瘝绫诲瀷
            if arity == -1:
                token_type = TokenType.VERB_VAR
            elif arity == 0:
                token_type = TokenType.VERB_0
            elif arity == 1:
                token_type = TokenType.VERB_1
            elif arity == 2:
                token_type = TokenType.VERB_2
            elif arity == 3:
                token_type = TokenType.VERB_3
            else:
                token_type = TokenType.VERB_VAR
            
            return Token(token_type, segment, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负甯冨皵瀛楅潰閲?        if segment in ('鐪?, '鍋?, 'true', 'false', 'True', 'False'):
            value = segment in ('鐪?, 'true', 'True')
            return Token(TokenType.BOOLEAN, value, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负绌哄€?        if segment == '绌?:
            return Token(TokenType.NULL, None, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负鏁板瓧
        if segment.isdigit() or (segment.replace('.', '', 1).isdigit() and segment.count('.') == 1):
            try:
                if '.' in segment:
                    value = float(segment)
                else:
                    value = int(segment)
                return Token(TokenType.NUMBER, value, line_num, column, segment)
            except ValueError:
                pass
        
        # 妫€鏌ユ槸鍚︿负涓枃鏁板瓧
        if all(c in self.chinese_numbers for c in segment):
            value = self._chinese_to_arabic(segment)
            return Token(TokenType.CHINESE_NUMBER, value, line_num, column, segment)
        
        # 鏅€氭爣璇嗙
        return Token(TokenType.IDENTIFIER, segment, line_num, column, segment)
    
    def _parse_string_literal(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽瀛楃涓插瓧闈㈤噺"""
        quote_char = line[start]
        position = start + 1
        value = ''
        
        while position < len(line):
            char = line[position]
            
            if char == quote_char:
                # 缁撴潫寮曞彿
                position += 1
                break
            elif char == '\\' and position + 1 < len(line):
                # 杞箟瀛楃
                next_char = line[position + 1]
                if next_char in ('n', 't', '\\', '"', "'"):
                    value += self._escape_char(next_char)
                    position += 2
                else:
                    value += char
                    position += 1
            else:
                value += char
                position += 1
        
        lexeme = line[start:position]
        return Token(TokenType.STRING, value, line_num, column, lexeme)
    
    def _escape_char(self, char: str) -> str:
        """杞箟瀛楃"""
        escape_map = {
            'n': '\n',
            't': '\t',
            '\\': '\\',
            '"': '"',
            "'": "'",
        }
        return escape_map.get(char, char)
    
    def _parse_number(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽鏁板瓧瀛楅潰閲?""
        position = start
        
        # 瑙ｆ瀽鏁存暟閮ㄥ垎
        while position < len(line) and line[position].isdigit():
            position += 1
        
        # 瑙ｆ瀽灏忔暟閮ㄥ垎
        if position < len(line) and line[position] == '.':
            position += 1
            while position < len(line) and line[position].isdigit():
                position += 1
        
        # 瑙ｆ瀽绉戝璁℃暟娉?        if position < len(line) and line[position].lower() == 'e':
            position += 1
            if position < len(line) and line[position] in ('+', '-'):
                position += 1
            while position < len(line) and line[position].isdigit():
                position += 1
        
        lexeme = line[start:position]
        
        # 灏濊瘯杞崲涓烘暟瀛?        try:
            if '.' in lexeme or 'e' in lexeme.lower():
                value = float(lexeme)
            else:
                value = int(lexeme)
        except ValueError:
            value = lexeme  # 淇濇寔鍘熸牱
        
        return Token(TokenType.NUMBER, value, line_num, column, lexeme)
    
    def _parse_chinese_number(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽涓枃鏁板瓧"""
        position = start
        lexeme = ''
        
        while position < len(line) and line[position] in self.chinese_numbers:
            lexeme += line[position]
            position += 1
        
        # 杞崲涓洪樋鎷変集鏁板瓧
        value = self._chinese_to_arabic(lexeme)
        
        return Token(TokenType.CHINESE_NUMBER, value, line_num, column, lexeme)
    
    def _chinese_to_arabic(self, chinese_num: str) -> int:
        """灏嗕腑鏂囨暟瀛楄浆鎹负闃挎媺浼暟瀛?""
        if not chinese_num:
            return 0
        
        # 绠€鍗曞疄鐜帮紝鍙鐞嗗熀鏈暟瀛?        total = 0
        current = 0
        
        for char in chinese_num:
            num = self.chinese_numbers.get(char, 0)
            
            if num < 10:
                current = num
            elif num >= 10:
                if current == 0:
                    current = 1
                total += current * num
                current = 0
        
        total += current
        return total
    
    def _parse_identifier(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽鏍囪瘑绗?""
        position = start
        
        # 鏀堕泦鏍囪瘑绗﹀瓧绗?        while position < len(line) and self._is_identifier_char(line[position]):
            position += 1
        
        lexeme = line[start:position]
        
        # 妫€鏌ユ槸鍚︿负鍏抽敭璇?        token_type = self._get_keyword_type(lexeme)
        if token_type:
            return Token(token_type, lexeme, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负鐧惧濮撳彉閲?        if self._is_bai_jia_xing(lexeme):
            return Token(TokenType.BAIJIAXING, lexeme, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负鍔ㄨ瘝
        arity = get_verb_arity(lexeme)
        if arity != 0:
            # 鏍规嵁鍏冩暟纭畾鍔ㄨ瘝绫诲瀷
            if arity == -1:
                token_type = TokenType.VERB_VAR
            elif arity == 0:
                token_type = TokenType.VERB_0
            elif arity == 1:
                token_type = TokenType.VERB_1
            elif arity == 2:
                token_type = TokenType.VERB_2
            elif arity == 3:
                token_type = TokenType.VERB_3
            else:
                token_type = TokenType.VERB_VAR
            
            return Token(token_type, lexeme, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负甯冨皵瀛楅潰閲?        if lexeme in ('鐪?, '鍋?, 'true', 'false', 'True', 'False'):
            value = lexeme in ('鐪?, 'true', 'True')
            return Token(TokenType.BOOLEAN, value, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负绌哄€?        if lexeme == '绌?:
            return Token(TokenType.NULL, None, line_num, column, lexeme)
        
        # 灏濊瘯涓枃鍒嗚瘝
        if len(lexeme) > 1 and any('\u4e00' <= c <= '\u9fff' for c in lexeme):
            # 浣跨敤jieba杩涜涓枃鍒嗚瘝
            segments = self._segment(lexeme)
            if len(segments) > 1:
                # 濡傛灉鏄涓瘝锛岃繑鍥炵涓€涓瘝浣滀负鏍囪瘑绗?                first_segment = segments[0]
                # 閫掑綊澶勭悊绗竴涓瘝
                return self._parse_identifier(first_segment, 0, line_num, column)
        
        # 鏅€氭爣璇嗙
        return Token(TokenType.IDENTIFIER, lexeme, line_num, column, lexeme)
    
    def _is_identifier_char(self, char: str) -> bool:
        """妫€鏌ュ瓧绗︽槸鍚︿负鏍囪瘑绗﹀瓧绗?""
        # 涓枃瀛楃銆佽嫳鏂囧瓧姣嶃€佹暟瀛椼€佷笅鍒掔嚎
        return ('\u4e00' <= char <= '\u9fff' or
                'a' <= char <= 'z' or
                'A' <= char <= 'Z' or
                char.isdigit() or
                char == '_')
    
    def _get_keyword_type(self, lexeme: str) -> Optional[TokenType]:
        """鑾峰彇鍏抽敭璇嶇被鍨?""
        # 妫€鏌ョ姸鎬佸叧閿瘝锛堝瀛楋級
        for keyword, token_type in self.state_keywords.items():
            if lexeme.startswith(keyword):
                return token_type
        
        # 妫€鏌ユ劅鐭ュ叧閿瘝锛堝瀛楋級
        for keyword, token_type in self.perception_keywords.items():
            if lexeme.startswith(keyword):
                return token_type
        
        # 妫€鏌ユ椂闂村叧閿瘝锛堝瀛楋級
        for keyword, token_type in self.time_keywords.items():
            if lexeme.startswith(keyword):
                return token_type
        
        # 妫€鏌ユ櫘閫氬叧閿瘝
        return self.keywords.get(lexeme)
    
    def _is_bai_jia_xing(self, lexeme: str) -> bool:
        """妫€鏌ユ槸鍚︿负鐧惧濮撳彉閲?""
        if not lexeme:
            return False
        
        # 鑾峰彇濮撴皬锛堢涓€涓瓧绗︼級
        surname = lexeme[0]
        
        # 妫€鏌ユ槸鍚︿负鍐茬獊濮撴皬
        if surname in self.conflict_surnames:
            return False
        
        # 妫€鏌ユ槸鍚︿负鐧惧濮?        return surname in self.bai_jia_xing
    
    def print_tokens(self, tokens: List[Token]) -> None:
        """鎵撳嵃璇嶆硶鍗曞厓鍒楄〃"""
        print("璇嶆硶鍒嗘瀽缁撴灉:")
        print("=" * 80)
        print(f"{'琛?:<4} {'鍒?:<4} {'绫诲瀷':<20} {'鍊?:<20} {'璇嶇礌':<20}")
        print("-" * 80)
        
        for token in tokens:
            value_str = str(token.value)
            if len(value_str) > 18:
                value_str = value_str[:15] + "..."
            
            lexeme_str = token.lexeme
            if len(lexeme_str) > 18:
                lexeme_str = lexeme_str[:15] + "..."
            
            print(f"{token.line:<4} {token.column:<4} {token.type.value:<20} {value_str:<20} {lexeme_str:<20}")
        
        print("=" * 80)


# 娴嬭瘯鍑芥暟
def test_lexer():
    """娴嬭瘯璇嶆硶鍒嗘瀽鍣?""
    print("璇嶆硶鍒嗘瀽鍣ㄦ祴璇?)
    print("=" * 50)
    
    lexer = YanLuLexer()
    
    # 娴嬭瘯鐢ㄤ緥
    test_cases = [
        (
            "瀹氭俯搴︽槸25銆?,
            "鍙橀噺瀹氫箟"
        ),
        (
            "濡傛灉娓╁害澶?0灏卞紑鍚鎵囥€?,
            "鏉′欢璇彞"
        ),
        (
            "瀵逛簬i鍦?鍒?0锛氬嵃i銆?,
            "寰幆璇彞"
        ),
        (
            "娓╁害鍙樹负30搴︺€?,
            "鐘舵€佽浆鎹?
        ),
        (
            "寮犱笁銆佹潕鍥涳紝璁＄畻鎶樻墸銆?,
            "鎰忓悎寮忓嚱鏁拌皟鐢?
        ),
        (
            "'浣犲ソ锛屼笘鐣?",
            "瀛楃涓插瓧闈㈤噺"
        ),
        (
            "鐪熶笖鍋?,
            "甯冨皵杩愮畻"
        ),
        (
            "瀹歺绛変簬鍗佸姞浜斻€?,
            "涓枃鏁板瓧"
        ),
    ]
    
    for source_code, description in test_cases:
        print(f"\n娴嬭瘯: {description}")
        print(f"婧愪唬鐮? {source_code}")
        
        try:
            tokens = lexer.tokenize(source_code)
            lexer.print_tokens(tokens)
        except Exception as e:
            print(f"閿欒: {e}")
    
    print("=" * 50)
    print("娴嬭瘯瀹屾垚")


if __name__ == "__main__":
    test_lexer())
        self.identifier_pattern = re.compile(r'^[\u4e00-\u9fffA-Za-z_][\u4e00-\u9fffA-Za-z0-9_]*
        """
        灏嗘簮浠ｇ爜杞崲涓鸿瘝娉曞崟鍏冨垪琛?        
        Args:
            source_code: 婧愪唬鐮佸瓧绗︿覆
            
        Returns:
            璇嶆硶鍗曞厓鍒楄〃
        """
        tokens = []
        lines = source_code.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            line_tokens = self._tokenize_line(line, line_num)
            tokens.extend(line_tokens)
            
            # 娣诲姞鎹㈣绗︼紙闄ら潪鏄渶鍚庝竴琛岋級
            if line_num < len(lines):
                tokens.append(Token(TokenType.NEWLINE, '\n', line_num, len(line) + 1, '\n'))
        
        # 娣诲姞鏂囦欢缁撴潫鏍囪
        tokens.append(Token(TokenType.EOF, '', len(lines) + 1, 1, ''))
        
        return tokens
    
    def _tokenize_line(self, line: str, line_num: int) -> List[Token]:
        """灏嗕竴琛屼唬鐮佽浆鎹负璇嶆硶鍗曞厓鍒楄〃"""
        tokens = []
        position = 0
        column = 1
        
        # 浣跨敤鍒嗚瘝鍣ㄨ繘琛屼腑鏂囧垎璇?        segments = self._segment(line)
        segment_index = 0
        
        while position < len(line):
            # 璺宠繃绌虹櫧瀛楃
            if line[position].isspace():
                if line[position] == '\n':
                    tokens.append(Token(TokenType.NEWLINE, '\n', line_num, column, '\n'))
                position += 1
                column += 1
                continue
            
            # 澶勭悊娉ㄩ噴
            if line[position] == '#':
                # 鍗曡娉ㄩ噴锛岃烦杩囨暣琛?                comment = line[position:]
                tokens.append(Token(TokenType.COMMENT, comment, line_num, column, comment))
                break
            
            # 澶勭悊澶氳瑷€浠ｇ爜鍧?            if line[position:position+2] == '{{':
                tokens.append(Token(TokenType.CODE_BLOCK_START, '{{', line_num, column, '{{'))
                position += 2
                column += 2
                continue
            
            if line[position:position+2] == '}}':
                tokens.append(Token(TokenType.CODE_BLOCK_END, '}}', line_num, column, '}}'))
                position += 2
                column += 2
                continue
            
            # 澶勭悊涓枃鏍囩偣绗﹀彿
            if line[position] in self.chinese_punctuation:
                char = line[position]
                token_type = self.chinese_punctuation[char]
                
                # 澶勭悊鎴愬鏍囩偣绗﹀彿
                if char in ('銆?, '銆?):
                    # 鏌ユ壘鍖归厤鐨勭粨鏉熺鍙?                    end_pos = line.find('銆? if char == '銆? else '銆?, position + 1)
                    if end_pos != -1:
                        value = line[position:end_pos + 1]
                        tokens.append(Token(token_type, value, line_num, column, value))
                        position = end_pos + 1
                        column += len(value)
                        continue
                
                tokens.append(Token(token_type, char, line_num, column, char))
                position += 1
                column += 1
                continue
            
            # 澶勭悊鐪佺暐鍙?            if line[position:position+2] == '鈥︹€?:
                tokens.append(Token(TokenType.ELLIPSIS, '鈥︹€?, line_num, column, '鈥︹€?))
                position += 2
                column += 2
                continue
            
            # 澶勭悊鐮存姌鍙?            if line[position:position+2] == '鈥斺€?:
                tokens.append(Token(TokenType.DASH, '鈥斺€?, line_num, column, '鈥斺€?))
                position += 2
                column += 2
                continue
            
            # 澶勭悊鍦嗗湀鍙?            if line[position] in '鈶犫憽鈶⑩懀鈶も懃鈶︹懅鈶ㄢ懇':
                tokens.append(Token(TokenType.CIRCLED_NUMBERS, line[position], line_num, column, line[position]))
                position += 1
                column += 1
                continue
            
            # 澶勭悊杩愮畻绗?            if line[position] in self.operators:
                # 妫€鏌ュ弻瀛楃杩愮畻绗?                if position + 1 < len(line):
                    two_char = line[position:position+2]
                    if two_char in ('鈮?, '鈮?, '鈮?):
                        tokens.append(Token(self.operators[two_char], two_char, line_num, column, two_char))
                        position += 2
                        column += 2
                        continue
                
                tokens.append(Token(self.operators[line[position]], line[position], line_num, column, line[position]))
                position += 1
                column += 1
                continue
            
            # 澶勭悊鍒嗙粍绗﹀彿
            if line[position] in self.grouping_symbols:
                tokens.append(Token(self.grouping_symbols[line[position]], line[position], line_num, column, line[position]))
                position += 1
                column += 1
                continue
            
            # 澶勭悊瀛楃涓插瓧闈㈤噺
            if line[position] in ('"', "'"):
                string_token = self._parse_string_literal(line, position, line_num, column)
                tokens.append(string_token)
                position += len(string_token.lexeme)
                column += len(string_token.lexeme)
                continue
            
            # 澶勭悊鏁板瓧瀛楅潰閲?            if line[position].isdigit() or (line[position] == '.' and position + 1 < len(line) and line[position + 1].isdigit()):
                number_token = self._parse_number(line, position, line_num, column)
                tokens.append(number_token)
                position += len(number_token.lexeme)
                column += len(number_token.lexeme)
                continue
            
            # 澶勭悊涓枃鏁板瓧
            if line[position] in self.chinese_numbers:
                chinese_number_token = self._parse_chinese_number(line, position, line_num, column)
                tokens.append(chinese_number_token)
                position += len(chinese_number_token.lexeme)
                column += len(chinese_number_token.lexeme)
                continue
            
            # 澶勭悊褰撳墠鍒嗚瘝娈?            if segment_index < len(segments):
                segment = segments[segment_index].strip()
                if segment:  # 璺宠繃绌哄垎璇?                    # 澶勭悊鍒嗚瘝娈?                    token = self._process_segment(segment, line_num, column)
                    tokens.append(token)
                    position += len(segment)
                    column += len(segment)
                segment_index += 1
            else:
                # 濡傛灉娌℃湁鏇村鍒嗚瘝锛屽鐞嗗墿浣欏瓧绗?                identifier_token = self._parse_identifier(line, position, line_num, column)
                tokens.append(identifier_token)
                position += len(identifier_token.lexeme)
                column += len(identifier_token.lexeme)
        
        return tokens
    
    def _process_segment(self, segment: str, line_num: int, column: int) -> Token:
        """澶勭悊鍒嗚瘝娈?""
        # 妫€鏌ユ槸鍚︿负鍏抽敭璇?        token_type = self._get_keyword_type(segment)
        if token_type:
            return Token(token_type, segment, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负鐧惧濮撳彉閲?        if self._is_bai_jia_xing(segment):
            return Token(TokenType.BAIJIAXING, segment, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负鍔ㄨ瘝
        arity = get_verb_arity(segment)
        if arity != 0:
            # 鏍规嵁鍏冩暟纭畾鍔ㄨ瘝绫诲瀷
            if arity == -1:
                token_type = TokenType.VERB_VAR
            elif arity == 0:
                token_type = TokenType.VERB_0
            elif arity == 1:
                token_type = TokenType.VERB_1
            elif arity == 2:
                token_type = TokenType.VERB_2
            elif arity == 3:
                token_type = TokenType.VERB_3
            else:
                token_type = TokenType.VERB_VAR
            
            return Token(token_type, segment, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负甯冨皵瀛楅潰閲?        if segment in ('鐪?, '鍋?, 'true', 'false', 'True', 'False'):
            value = segment in ('鐪?, 'true', 'True')
            return Token(TokenType.BOOLEAN, value, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负绌哄€?        if segment == '绌?:
            return Token(TokenType.NULL, None, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负鏁板瓧
        if segment.isdigit() or (segment.replace('.', '', 1).isdigit() and segment.count('.') == 1):
            try:
                if '.' in segment:
                    value = float(segment)
                else:
                    value = int(segment)
                return Token(TokenType.NUMBER, value, line_num, column, segment)
            except ValueError:
                pass
        
        # 妫€鏌ユ槸鍚︿负涓枃鏁板瓧
        if all(c in self.chinese_numbers for c in segment):
            value = self._chinese_to_arabic(segment)
            return Token(TokenType.CHINESE_NUMBER, value, line_num, column, segment)
        
        # 鏅€氭爣璇嗙
        return Token(TokenType.IDENTIFIER, segment, line_num, column, segment)
    
    def _parse_string_literal(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽瀛楃涓插瓧闈㈤噺"""
        quote_char = line[start]
        position = start + 1
        value = ''
        
        while position < len(line):
            char = line[position]
            
            if char == quote_char:
                # 缁撴潫寮曞彿
                position += 1
                break
            elif char == '\\' and position + 1 < len(line):
                # 杞箟瀛楃
                next_char = line[position + 1]
                if next_char in ('n', 't', '\\', '"', "'"):
                    value += self._escape_char(next_char)
                    position += 2
                else:
                    value += char
                    position += 1
            else:
                value += char
                position += 1
        
        lexeme = line[start:position]
        return Token(TokenType.STRING, value, line_num, column, lexeme)
    
    def _escape_char(self, char: str) -> str:
        """杞箟瀛楃"""
        escape_map = {
            'n': '\n',
            't': '\t',
            '\\': '\\',
            '"': '"',
            "'": "'",
        }
        return escape_map.get(char, char)
    
    def _parse_number(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽鏁板瓧瀛楅潰閲?""
        position = start
        
        # 瑙ｆ瀽鏁存暟閮ㄥ垎
        while position < len(line) and line[position].isdigit():
            position += 1
        
        # 瑙ｆ瀽灏忔暟閮ㄥ垎
        if position < len(line) and line[position] == '.':
            position += 1
            while position < len(line) and line[position].isdigit():
                position += 1
        
        # 瑙ｆ瀽绉戝璁℃暟娉?        if position < len(line) and line[position].lower() == 'e':
            position += 1
            if position < len(line) and line[position] in ('+', '-'):
                position += 1
            while position < len(line) and line[position].isdigit():
                position += 1
        
        lexeme = line[start:position]
        
        # 灏濊瘯杞崲涓烘暟瀛?        try:
            if '.' in lexeme or 'e' in lexeme.lower():
                value = float(lexeme)
            else:
                value = int(lexeme)
        except ValueError:
            value = lexeme  # 淇濇寔鍘熸牱
        
        return Token(TokenType.NUMBER, value, line_num, column, lexeme)
    
    def _parse_chinese_number(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽涓枃鏁板瓧"""
        position = start
        lexeme = ''
        
        while position < len(line) and line[position] in self.chinese_numbers:
            lexeme += line[position]
            position += 1
        
        # 杞崲涓洪樋鎷変集鏁板瓧
        value = self._chinese_to_arabic(lexeme)
        
        return Token(TokenType.CHINESE_NUMBER, value, line_num, column, lexeme)
    
    def _chinese_to_arabic(self, chinese_num: str) -> int:
        """灏嗕腑鏂囨暟瀛楄浆鎹负闃挎媺浼暟瀛?""
        if not chinese_num:
            return 0
        
        # 绠€鍗曞疄鐜帮紝鍙鐞嗗熀鏈暟瀛?        total = 0
        current = 0
        
        for char in chinese_num:
            num = self.chinese_numbers.get(char, 0)
            
            if num < 10:
                current = num
            elif num >= 10:
                if current == 0:
                    current = 1
                total += current * num
                current = 0
        
        total += current
        return total
    
    def _parse_identifier(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽鏍囪瘑绗?""
        position = start
        
        # 鏀堕泦鏍囪瘑绗﹀瓧绗?        while position < len(line) and self._is_identifier_char(line[position]):
            position += 1
        
        lexeme = line[start:position]
        
        # 妫€鏌ユ槸鍚︿负鍏抽敭璇?        token_type = self._get_keyword_type(lexeme)
        if token_type:
            return Token(token_type, lexeme, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负鐧惧濮撳彉閲?        if self._is_bai_jia_xing(lexeme):
            return Token(TokenType.BAIJIAXING, lexeme, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负鍔ㄨ瘝
        arity = get_verb_arity(lexeme)
        if arity != 0:
            # 鏍规嵁鍏冩暟纭畾鍔ㄨ瘝绫诲瀷
            if arity == -1:
                token_type = TokenType.VERB_VAR
            elif arity == 0:
                token_type = TokenType.VERB_0
            elif arity == 1:
                token_type = TokenType.VERB_1
            elif arity == 2:
                token_type = TokenType.VERB_2
            elif arity == 3:
                token_type = TokenType.VERB_3
            else:
                token_type = TokenType.VERB_VAR
            
            return Token(token_type, lexeme, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负甯冨皵瀛楅潰閲?        if lexeme in ('鐪?, '鍋?, 'true', 'false', 'True', 'False'):
            value = lexeme in ('鐪?, 'true', 'True')
            return Token(TokenType.BOOLEAN, value, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负绌哄€?        if lexeme == '绌?:
            return Token(TokenType.NULL, None, line_num, column, lexeme)
        
        # 灏濊瘯涓枃鍒嗚瘝
        if len(lexeme) > 1 and any('\u4e00' <= c <= '\u9fff' for c in lexeme):
            # 浣跨敤jieba杩涜涓枃鍒嗚瘝
            segments = self._segment(lexeme)
            if len(segments) > 1:
                # 濡傛灉鏄涓瘝锛岃繑鍥炵涓€涓瘝浣滀负鏍囪瘑绗?                first_segment = segments[0]
                # 閫掑綊澶勭悊绗竴涓瘝
                return self._parse_identifier(first_segment, 0, line_num, column)
        
        # 鏅€氭爣璇嗙
        return Token(TokenType.IDENTIFIER, lexeme, line_num, column, lexeme)
    
    def _is_identifier_char(self, char: str) -> bool:
        """妫€鏌ュ瓧绗︽槸鍚︿负鏍囪瘑绗﹀瓧绗?""
        # 涓枃瀛楃銆佽嫳鏂囧瓧姣嶃€佹暟瀛椼€佷笅鍒掔嚎
        return ('\u4e00' <= char <= '\u9fff' or
                'a' <= char <= 'z' or
                'A' <= char <= 'Z' or
                char.isdigit() or
                char == '_')
    
    def _get_keyword_type(self, lexeme: str) -> Optional[TokenType]:
        """鑾峰彇鍏抽敭璇嶇被鍨?""
        # 妫€鏌ョ姸鎬佸叧閿瘝锛堝瀛楋級
        for keyword, token_type in self.state_keywords.items():
            if lexeme.startswith(keyword):
                return token_type
        
        # 妫€鏌ユ劅鐭ュ叧閿瘝锛堝瀛楋級
        for keyword, token_type in self.perception_keywords.items():
            if lexeme.startswith(keyword):
                return token_type
        
        # 妫€鏌ユ椂闂村叧閿瘝锛堝瀛楋級
        for keyword, token_type in self.time_keywords.items():
            if lexeme.startswith(keyword):
                return token_type
        
        # 妫€鏌ユ櫘閫氬叧閿瘝
        return self.keywords.get(lexeme)
    
    def _is_bai_jia_xing(self, lexeme: str) -> bool:
        """妫€鏌ユ槸鍚︿负鐧惧濮撳彉閲?""
        if not lexeme:
            return False
        
        # 鑾峰彇濮撴皬锛堢涓€涓瓧绗︼級
        surname = lexeme[0]
        
        # 妫€鏌ユ槸鍚︿负鍐茬獊濮撴皬
        if surname in self.conflict_surnames:
            return False
        
        # 妫€鏌ユ槸鍚︿负鐧惧濮?        return surname in self.bai_jia_xing
    
    def print_tokens(self, tokens: List[Token]) -> None:
        """鎵撳嵃璇嶆硶鍗曞厓鍒楄〃"""
        print("璇嶆硶鍒嗘瀽缁撴灉:")
        print("=" * 80)
        print(f"{'琛?:<4} {'鍒?:<4} {'绫诲瀷':<20} {'鍊?:<20} {'璇嶇礌':<20}")
        print("-" * 80)
        
        for token in tokens:
            value_str = str(token.value)
            if len(value_str) > 18:
                value_str = value_str[:15] + "..."
            
            lexeme_str = token.lexeme
            if len(lexeme_str) > 18:
                lexeme_str = lexeme_str[:15] + "..."
            
            print(f"{token.line:<4} {token.column:<4} {token.type.value:<20} {value_str:<20} {lexeme_str:<20}")
        
        print("=" * 80)


# 娴嬭瘯鍑芥暟
def test_lexer():
    """娴嬭瘯璇嶆硶鍒嗘瀽鍣?""
    print("璇嶆硶鍒嗘瀽鍣ㄦ祴璇?)
    print("=" * 50)
    
    lexer = YanLuLexer()
    
    # 娴嬭瘯鐢ㄤ緥
    test_cases = [
        (
            "瀹氭俯搴︽槸25銆?,
            "鍙橀噺瀹氫箟"
        ),
        (
            "濡傛灉娓╁害澶?0灏卞紑鍚鎵囥€?,
            "鏉′欢璇彞"
        ),
        (
            "瀵逛簬i鍦?鍒?0锛氬嵃i銆?,
            "寰幆璇彞"
        ),
        (
            "娓╁害鍙樹负30搴︺€?,
            "鐘舵€佽浆鎹?
        ),
        (
            "寮犱笁銆佹潕鍥涳紝璁＄畻鎶樻墸銆?,
            "鎰忓悎寮忓嚱鏁拌皟鐢?
        ),
        (
            "'浣犲ソ锛屼笘鐣?",
            "瀛楃涓插瓧闈㈤噺"
        ),
        (
            "鐪熶笖鍋?,
            "甯冨皵杩愮畻"
        ),
        (
            "瀹歺绛変簬鍗佸姞浜斻€?,
            "涓枃鏁板瓧"
        ),
    ]
    
    for source_code, description in test_cases:
        print(f"\n娴嬭瘯: {description}")
        print(f"婧愪唬鐮? {source_code}")
        
        try:
            tokens = lexer.tokenize(source_code)
            lexer.print_tokens(tokens)
        except Exception as e:
            print(f"閿欒: {e}")
    
    print("=" * 50)
    print("娴嬭瘯瀹屾垚")


if __name__ == "__main__":
    test_lexer())
    
    def _init_segmenter(self):
        """鍒濆鍖栧垎璇嶅櫒"""
        if self.segmenter_type == "thulac":
            try:
                import thulac
                # 浣跨敤seg_only=True鍙繘琛屽垎璇嶏紝涓嶈繘琛岃瘝鎬ф爣娉?                self.segmenter = thulac.thulac(seg_only=True, model_path=None)
                print(f"浣跨敤THULAC鍒嗚瘝鍣?(seg_only妯″紡)")
            except ImportError:
                print("璀﹀憡: 鏈畨瑁匱HULAC锛屽洖閫€鍒癹ieba鍒嗚瘝鍣?)
                print("瀹夎鍛戒护: pip install thulac")
                self.segmenter_type = "jieba"
                self.segmenter = jieba
        else:
            # 榛樿浣跨敤jieba
            self.segmenter = jieba
            print(f"浣跨敤jieba鍒嗚瘝鍣?)
    
    def _segment(self, text: str) -> List[str]:
        """
        鍒嗚瘝鏂规硶
        
        Args:
            text: 寰呭垎璇嶇殑鏂囨湰
            
        Returns:
            鍒嗚瘝缁撴灉鍒楄〃
        """
        if self.segmenter_type == "thulac":
            # THULAC鍒嗚瘝
            result = self.segmenter.cut(text, text=True)
            return result.split()
        else:
            # jieba鍒嗚瘝
            return list(self.segmenter.lcut(text))
        
    def tokenize(self, source_code: str) -> List[Token]:
        """
        灏嗘簮浠ｇ爜杞崲涓鸿瘝娉曞崟鍏冨垪琛?        
        Args:
            source_code: 婧愪唬鐮佸瓧绗︿覆
            
        Returns:
            璇嶆硶鍗曞厓鍒楄〃
        """
        tokens = []
        lines = source_code.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            line_tokens = self._tokenize_line(line, line_num)
            tokens.extend(line_tokens)
            
            # 娣诲姞鎹㈣绗︼紙闄ら潪鏄渶鍚庝竴琛岋級
            if line_num < len(lines):
                tokens.append(Token(TokenType.NEWLINE, '\n', line_num, len(line) + 1, '\n'))
        
        # 娣诲姞鏂囦欢缁撴潫鏍囪
        tokens.append(Token(TokenType.EOF, '', len(lines) + 1, 1, ''))
        
        return tokens
    
    def _tokenize_line(self, line: str, line_num: int) -> List[Token]:
        """灏嗕竴琛屼唬鐮佽浆鎹负璇嶆硶鍗曞厓鍒楄〃"""
        tokens = []
        position = 0
        column = 1
        
        # 浣跨敤鍒嗚瘝鍣ㄨ繘琛屼腑鏂囧垎璇?        segments = self._segment(line)
        segment_index = 0
        
        while position < len(line):
            # 璺宠繃绌虹櫧瀛楃
            if line[position].isspace():
                if line[position] == '\n':
                    tokens.append(Token(TokenType.NEWLINE, '\n', line_num, column, '\n'))
                position += 1
                column += 1
                continue
            
            # 澶勭悊娉ㄩ噴
            if line[position] == '#':
                # 鍗曡娉ㄩ噴锛岃烦杩囨暣琛?                comment = line[position:]
                tokens.append(Token(TokenType.COMMENT, comment, line_num, column, comment))
                break
            
            # 澶勭悊澶氳瑷€浠ｇ爜鍧?            if line[position:position+2] == '{{':
                tokens.append(Token(TokenType.CODE_BLOCK_START, '{{', line_num, column, '{{'))
                position += 2
                column += 2
                continue
            
            if line[position:position+2] == '}}':
                tokens.append(Token(TokenType.CODE_BLOCK_END, '}}', line_num, column, '}}'))
                position += 2
                column += 2
                continue
            
            # 澶勭悊涓枃鏍囩偣绗﹀彿
            if line[position] in self.chinese_punctuation:
                char = line[position]
                token_type = self.chinese_punctuation[char]
                
                # 澶勭悊鎴愬鏍囩偣绗﹀彿
                if char in ('銆?, '銆?):
                    # 鏌ユ壘鍖归厤鐨勭粨鏉熺鍙?                    end_pos = line.find('銆? if char == '銆? else '銆?, position + 1)
                    if end_pos != -1:
                        value = line[position:end_pos + 1]
                        tokens.append(Token(token_type, value, line_num, column, value))
                        position = end_pos + 1
                        column += len(value)
                        continue
                
                tokens.append(Token(token_type, char, line_num, column, char))
                position += 1
                column += 1
                continue
            
            # 澶勭悊鐪佺暐鍙?            if line[position:position+2] == '鈥︹€?:
                tokens.append(Token(TokenType.ELLIPSIS, '鈥︹€?, line_num, column, '鈥︹€?))
                position += 2
                column += 2
                continue
            
            # 澶勭悊鐮存姌鍙?            if line[position:position+2] == '鈥斺€?:
                tokens.append(Token(TokenType.DASH, '鈥斺€?, line_num, column, '鈥斺€?))
                position += 2
                column += 2
                continue
            
            # 澶勭悊鍦嗗湀鍙?            if line[position] in '鈶犫憽鈶⑩懀鈶も懃鈶︹懅鈶ㄢ懇':
                tokens.append(Token(TokenType.CIRCLED_NUMBERS, line[position], line_num, column, line[position]))
                position += 1
                column += 1
                continue
            
            # 澶勭悊杩愮畻绗?            if line[position] in self.operators:
                # 妫€鏌ュ弻瀛楃杩愮畻绗?                if position + 1 < len(line):
                    two_char = line[position:position+2]
                    if two_char in ('鈮?, '鈮?, '鈮?):
                        tokens.append(Token(self.operators[two_char], two_char, line_num, column, two_char))
                        position += 2
                        column += 2
                        continue
                
                tokens.append(Token(self.operators[line[position]], line[position], line_num, column, line[position]))
                position += 1
                column += 1
                continue
            
            # 澶勭悊鍒嗙粍绗﹀彿
            if line[position] in self.grouping_symbols:
                tokens.append(Token(self.grouping_symbols[line[position]], line[position], line_num, column, line[position]))
                position += 1
                column += 1
                continue
            
            # 澶勭悊瀛楃涓插瓧闈㈤噺
            if line[position] in ('"', "'"):
                string_token = self._parse_string_literal(line, position, line_num, column)
                tokens.append(string_token)
                position += len(string_token.lexeme)
                column += len(string_token.lexeme)
                continue
            
            # 澶勭悊鏁板瓧瀛楅潰閲?            if line[position].isdigit() or (line[position] == '.' and position + 1 < len(line) and line[position + 1].isdigit()):
                number_token = self._parse_number(line, position, line_num, column)
                tokens.append(number_token)
                position += len(number_token.lexeme)
                column += len(number_token.lexeme)
                continue
            
            # 澶勭悊涓枃鏁板瓧
            if line[position] in self.chinese_numbers:
                chinese_number_token = self._parse_chinese_number(line, position, line_num, column)
                tokens.append(chinese_number_token)
                position += len(chinese_number_token.lexeme)
                column += len(chinese_number_token.lexeme)
                continue
            
            # 澶勭悊褰撳墠鍒嗚瘝娈?            if segment_index < len(segments):
                segment = segments[segment_index].strip()
                if segment:  # 璺宠繃绌哄垎璇?                    # 澶勭悊鍒嗚瘝娈?                    token = self._process_segment(segment, line_num, column)
                    tokens.append(token)
                    position += len(segment)
                    column += len(segment)
                segment_index += 1
            else:
                # 濡傛灉娌℃湁鏇村鍒嗚瘝锛屽鐞嗗墿浣欏瓧绗?                identifier_token = self._parse_identifier(line, position, line_num, column)
                tokens.append(identifier_token)
                position += len(identifier_token.lexeme)
                column += len(identifier_token.lexeme)
        
        return tokens
    
    def _process_segment(self, segment: str, line_num: int, column: int) -> Token:
        """澶勭悊鍒嗚瘝娈?""
        # 妫€鏌ユ槸鍚︿负鍏抽敭璇?        token_type = self._get_keyword_type(segment)
        if token_type:
            return Token(token_type, segment, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负鐧惧濮撳彉閲?        if self._is_bai_jia_xing(segment):
            return Token(TokenType.BAIJIAXING, segment, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负鍔ㄨ瘝
        arity = get_verb_arity(segment)
        if arity != 0:
            # 鏍规嵁鍏冩暟纭畾鍔ㄨ瘝绫诲瀷
            if arity == -1:
                token_type = TokenType.VERB_VAR
            elif arity == 0:
                token_type = TokenType.VERB_0
            elif arity == 1:
                token_type = TokenType.VERB_1
            elif arity == 2:
                token_type = TokenType.VERB_2
            elif arity == 3:
                token_type = TokenType.VERB_3
            else:
                token_type = TokenType.VERB_VAR
            
            return Token(token_type, segment, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负甯冨皵瀛楅潰閲?        if segment in ('鐪?, '鍋?, 'true', 'false', 'True', 'False'):
            value = segment in ('鐪?, 'true', 'True')
            return Token(TokenType.BOOLEAN, value, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负绌哄€?        if segment == '绌?:
            return Token(TokenType.NULL, None, line_num, column, segment)
        
        # 妫€鏌ユ槸鍚︿负鏁板瓧
        if segment.isdigit() or (segment.replace('.', '', 1).isdigit() and segment.count('.') == 1):
            try:
                if '.' in segment:
                    value = float(segment)
                else:
                    value = int(segment)
                return Token(TokenType.NUMBER, value, line_num, column, segment)
            except ValueError:
                pass
        
        # 妫€鏌ユ槸鍚︿负涓枃鏁板瓧
        if all(c in self.chinese_numbers for c in segment):
            value = self._chinese_to_arabic(segment)
            return Token(TokenType.CHINESE_NUMBER, value, line_num, column, segment)
        
        # 鏅€氭爣璇嗙
        return Token(TokenType.IDENTIFIER, segment, line_num, column, segment)
    
    def _parse_string_literal(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽瀛楃涓插瓧闈㈤噺"""
        quote_char = line[start]
        position = start + 1
        value = ''
        
        while position < len(line):
            char = line[position]
            
            if char == quote_char:
                # 缁撴潫寮曞彿
                position += 1
                break
            elif char == '\\' and position + 1 < len(line):
                # 杞箟瀛楃
                next_char = line[position + 1]
                if next_char in ('n', 't', '\\', '"', "'"):
                    value += self._escape_char(next_char)
                    position += 2
                else:
                    value += char
                    position += 1
            else:
                value += char
                position += 1
        
        lexeme = line[start:position]
        return Token(TokenType.STRING, value, line_num, column, lexeme)
    
    def _escape_char(self, char: str) -> str:
        """杞箟瀛楃"""
        escape_map = {
            'n': '\n',
            't': '\t',
            '\\': '\\',
            '"': '"',
            "'": "'",
        }
        return escape_map.get(char, char)
    
    def _parse_number(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽鏁板瓧瀛楅潰閲?""
        position = start
        
        # 瑙ｆ瀽鏁存暟閮ㄥ垎
        while position < len(line) and line[position].isdigit():
            position += 1
        
        # 瑙ｆ瀽灏忔暟閮ㄥ垎
        if position < len(line) and line[position] == '.':
            position += 1
            while position < len(line) and line[position].isdigit():
                position += 1
        
        # 瑙ｆ瀽绉戝璁℃暟娉?        if position < len(line) and line[position].lower() == 'e':
            position += 1
            if position < len(line) and line[position] in ('+', '-'):
                position += 1
            while position < len(line) and line[position].isdigit():
                position += 1
        
        lexeme = line[start:position]
        
        # 灏濊瘯杞崲涓烘暟瀛?        try:
            if '.' in lexeme or 'e' in lexeme.lower():
                value = float(lexeme)
            else:
                value = int(lexeme)
        except ValueError:
            value = lexeme  # 淇濇寔鍘熸牱
        
        return Token(TokenType.NUMBER, value, line_num, column, lexeme)
    
    def _parse_chinese_number(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽涓枃鏁板瓧"""
        position = start
        lexeme = ''
        
        while position < len(line) and line[position] in self.chinese_numbers:
            lexeme += line[position]
            position += 1
        
        # 杞崲涓洪樋鎷変集鏁板瓧
        value = self._chinese_to_arabic(lexeme)
        
        return Token(TokenType.CHINESE_NUMBER, value, line_num, column, lexeme)
    
    def _chinese_to_arabic(self, chinese_num: str) -> int:
        """灏嗕腑鏂囨暟瀛楄浆鎹负闃挎媺浼暟瀛?""
        if not chinese_num:
            return 0
        
        # 绠€鍗曞疄鐜帮紝鍙鐞嗗熀鏈暟瀛?        total = 0
        current = 0
        
        for char in chinese_num:
            num = self.chinese_numbers.get(char, 0)
            
            if num < 10:
                current = num
            elif num >= 10:
                if current == 0:
                    current = 1
                total += current * num
                current = 0
        
        total += current
        return total
    
    def _parse_identifier(self, line: str, start: int, line_num: int, column: int) -> Token:
        """瑙ｆ瀽鏍囪瘑绗?""
        position = start
        
        # 鏀堕泦鏍囪瘑绗﹀瓧绗?        while position < len(line) and self._is_identifier_char(line[position]):
            position += 1
        
        lexeme = line[start:position]
        
        # 妫€鏌ユ槸鍚︿负鍏抽敭璇?        token_type = self._get_keyword_type(lexeme)
        if token_type:
            return Token(token_type, lexeme, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负鐧惧濮撳彉閲?        if self._is_bai_jia_xing(lexeme):
            return Token(TokenType.BAIJIAXING, lexeme, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负鍔ㄨ瘝
        arity = get_verb_arity(lexeme)
        if arity != 0:
            # 鏍规嵁鍏冩暟纭畾鍔ㄨ瘝绫诲瀷
            if arity == -1:
                token_type = TokenType.VERB_VAR
            elif arity == 0:
                token_type = TokenType.VERB_0
            elif arity == 1:
                token_type = TokenType.VERB_1
            elif arity == 2:
                token_type = TokenType.VERB_2
            elif arity == 3:
                token_type = TokenType.VERB_3
            else:
                token_type = TokenType.VERB_VAR
            
            return Token(token_type, lexeme, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负甯冨皵瀛楅潰閲?        if lexeme in ('鐪?, '鍋?, 'true', 'false', 'True', 'False'):
            value = lexeme in ('鐪?, 'true', 'True')
            return Token(TokenType.BOOLEAN, value, line_num, column, lexeme)
        
        # 妫€鏌ユ槸鍚︿负绌哄€?        if lexeme == '绌?:
            return Token(TokenType.NULL, None, line_num, column, lexeme)
        
        # 灏濊瘯涓枃鍒嗚瘝
        if len(lexeme) > 1 and any('\u4e00' <= c <= '\u9fff' for c in lexeme):
            # 浣跨敤jieba杩涜涓枃鍒嗚瘝
            segments = self._segment(lexeme)
            if len(segments) > 1:
                # 濡傛灉鏄涓瘝锛岃繑鍥炵涓€涓瘝浣滀负鏍囪瘑绗?                first_segment = segments[0]
                # 閫掑綊澶勭悊绗竴涓瘝
                return self._parse_identifier(first_segment, 0, line_num, column)
        
        # 鏅€氭爣璇嗙
        return Token(TokenType.IDENTIFIER, lexeme, line_num, column, lexeme)
    
    def _is_identifier_char(self, char: str) -> bool:
        """妫€鏌ュ瓧绗︽槸鍚︿负鏍囪瘑绗﹀瓧绗?""
        # 涓枃瀛楃銆佽嫳鏂囧瓧姣嶃€佹暟瀛椼€佷笅鍒掔嚎
        return ('\u4e00' <= char <= '\u9fff' or
                'a' <= char <= 'z' or
                'A' <= char <= 'Z' or
                char.isdigit() or
                char == '_')
    
    def _get_keyword_type(self, lexeme: str) -> Optional[TokenType]:
        """鑾峰彇鍏抽敭璇嶇被鍨?""
        # 妫€鏌ョ姸鎬佸叧閿瘝锛堝瀛楋級
        for keyword, token_type in self.state_keywords.items():
            if lexeme.startswith(keyword):
                return token_type
        
        # 妫€鏌ユ劅鐭ュ叧閿瘝锛堝瀛楋級
        for keyword, token_type in self.perception_keywords.items():
            if lexeme.startswith(keyword):
                return token_type
        
        # 妫€鏌ユ椂闂村叧閿瘝锛堝瀛楋級
        for keyword, token_type in self.time_keywords.items():
            if lexeme.startswith(keyword):
                return token_type
        
        # 妫€鏌ユ櫘閫氬叧閿瘝
        return self.keywords.get(lexeme)
    
    def _is_bai_jia_xing(self, lexeme: str) -> bool:
        """妫€鏌ユ槸鍚︿负鐧惧濮撳彉閲?""
        if not lexeme:
            return False
        
        # 鑾峰彇濮撴皬锛堢涓€涓瓧绗︼級
        surname = lexeme[0]
        
        # 妫€鏌ユ槸鍚︿负鍐茬獊濮撴皬
        if surname in self.conflict_surnames:
            return False
        
        # 妫€鏌ユ槸鍚︿负鐧惧濮?        return surname in self.bai_jia_xing
    
    def print_tokens(self, tokens: List[Token]) -> None:
        """鎵撳嵃璇嶆硶鍗曞厓鍒楄〃"""
        print("璇嶆硶鍒嗘瀽缁撴灉:")
        print("=" * 80)
        print(f"{'琛?:<4} {'鍒?:<4} {'绫诲瀷':<20} {'鍊?:<20} {'璇嶇礌':<20}")
        print("-" * 80)
        
        for token in tokens:
            value_str = str(token.value)
            if len(value_str) > 18:
                value_str = value_str[:15] + "..."
            
            lexeme_str = token.lexeme
            if len(lexeme_str) > 18:
                lexeme_str = lexeme_str[:15] + "..."
            
            print(f"{token.line:<4} {token.column:<4} {token.type.value:<20} {value_str:<20} {lexeme_str:<20}")
        
        print("=" * 80)


# 娴嬭瘯鍑芥暟
def test_lexer():
    """娴嬭瘯璇嶆硶鍒嗘瀽鍣?""
    print("璇嶆硶鍒嗘瀽鍣ㄦ祴璇?)
    print("=" * 50)
    
    lexer = YanLuLexer()
    
    # 娴嬭瘯鐢ㄤ緥
    test_cases = [
        (
            "瀹氭俯搴︽槸25銆?,
            "鍙橀噺瀹氫箟"
        ),
        (
            "濡傛灉娓╁害澶?0灏卞紑鍚鎵囥€?,
            "鏉′欢璇彞"
        ),
        (
            "瀵逛簬i鍦?鍒?0锛氬嵃i銆?,
            "寰幆璇彞"
        ),
        (
            "娓╁害鍙樹负30搴︺€?,
            "鐘舵€佽浆鎹?
        ),
        (
            "寮犱笁銆佹潕鍥涳紝璁＄畻鎶樻墸銆?,
            "鎰忓悎寮忓嚱鏁拌皟鐢?
        ),
        (
            "'浣犲ソ锛屼笘鐣?",
            "瀛楃涓插瓧闈㈤噺"
        ),
        (
            "鐪熶笖鍋?,
            "甯冨皵杩愮畻"
        ),
        (
            "瀹歺绛変簬鍗佸姞浜斻€?,
            "涓枃鏁板瓧"
        ),
    ]
    
    for source_code, description in test_cases:
        print(f"\n娴嬭瘯: {description}")
        print(f"婧愪唬鐮? {source_code}")
        
        try:
            tokens = lexer.tokenize(source_code)
            lexer.print_tokens(tokens)
        except Exception as e:
            print(f"閿欒: {e}")
    
    print("=" * 50)
    print("娴嬭瘯瀹屾垚")


if __name__ == "__main__":
    test_lexer()
