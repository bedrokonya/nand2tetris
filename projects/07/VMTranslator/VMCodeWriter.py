import os
import typing as tp

from VMCommandTranslationProvider import VMCommandTranslationProvider
from VMConstant import VMCmd, VMSegment,\
    ARITHMETIC_COMMANDS, SEGMENT_TRANSLATION, TEMP_LOCATION_IN_RAM, IMPLEMENTATION_DIRECTORY


class VMCodeWriter:
    """
    Translates VM commands into Hack assembly code.
    """

    def __init__(self, asm_file_name: str, is_bootstrap_needed: bool):
        self._asm_file_name = asm_file_name
        self._vm_file_name = None
        self._vm_file_name_without_dir = None

        self._command_translation_provider = VMCommandTranslationProvider(IMPLEMENTATION_DIRECTORY)
        self._current_function_scope = None
        self._label_counter = 0

        self.result = ''

        if is_bootstrap_needed:
            self._write_init()

    def set_file_name(self, vm_file_name: str) -> None:
        """
        Informs VMCodeWriter that the translation of a new .vm file is started.

        :param vm_file_name: the name of file currently being translated
        """
        self._vm_file_name = vm_file_name
        self._vm_file_name_without_dir = os.path.basename(vm_file_name).rsplit('.', maxsplit=1)[0].strip()

    def write_asm_file(self) -> None:
        with open(self._asm_file_name, 'w') as asm_file:
            asm_file.write(self.result)

    def write_command(self, command_name: str, arg1: tp.Optional[str], arg2: tp.Optional[str]) -> None:
        if command_name in ARITHMETIC_COMMANDS:
            self._write_arithmetic(command_name)
        if command_name in [VMCmd.C_PUSH, VMCmd.C_POP]:
            self._write_push_pop(command_name, arg1, arg2)
        if command_name == VMCmd.C_LABEL:
            self._write_label(arg1)
        if command_name == VMCmd.C_GOTO:
            self._write_goto(arg1)
        if command_name == VMCmd.C_IF:
            self._write_if(arg1)
        if command_name == VMCmd.C_FUNCTION:
            self._write_function(arg1, arg2)
        if command_name == VMCmd.C_CALL:
            self._write_call(arg1, arg2)
        if command_name == VMCmd.C_RETURN:
            self._write_return()

    def _get_label_counter(self) -> int:
        current_counter: int = self._label_counter
        self._label_counter += 1
        return current_counter

    def _write_init(self) -> None:
        """
        Writes assembly code that affects the VM initialization, also called bootstrap code.
        This code will be placed at the beginning of the output file.
        """
        label_num: int = self._get_label_counter()
        translated_command: str = self._command_translation_provider.get_command_translation(VMCmd.C_INIT)
        translated_command += self._command_translation_provider.get_command_translation(VMCmd.C_CALL) \
            .format('Sys.init', label_num, 0, 'Sys.init', 'Sys.init', label_num)

        self.result += translated_command

    def _write_arithmetic(self, command_name: str) -> None:
        label_num: int = self._get_label_counter()
        translated_command = self._command_translation_provider.get_command_translation(command_name)
        if command_name in [VMCmd.C_EQ, VMCmd.C_GT, VMCmd.C_LT]:
            translated_command = translated_command.format(label_num, label_num, label_num, label_num)

        self.result += translated_command

    def _write_push_pop(self, command_name: str, segment: str, i: str) -> None:
        translated_command = self._command_translation_provider.get_command_translation(command_name, segment)
        if segment == VMSegment.S_CONSTANT:
            translated_command = translated_command.format(i)
        if segment in [VMSegment.S_LOCAL, VMSegment.S_ARGUMENT, VMSegment.S_THIS, VMSegment.S_THAT]:
            translated_command = translated_command.format(i, SEGMENT_TRANSLATION.get(segment))
        if segment == VMSegment.S_STATIC:
            translated_command = translated_command.format(self._vm_file_name_without_dir, i)
        if segment == VMSegment.S_TEMP:
            translated_command = translated_command.format(TEMP_LOCATION_IN_RAM, i)
        if segment == VMSegment.S_POINTER:
            new_segment = VMSegment.S_THIS if int(i) == 0 else VMSegment.S_THAT
            translated_command = translated_command.format(SEGMENT_TRANSLATION.get(new_segment))

        self.result += translated_command

    def _write_label(self, label: str) -> None:
        translated_command = self._command_translation_provider.get_command_translation(VMCmd.C_LABEL)\
            .format(str(self._current_function_scope), label)

        self.result += translated_command

    def _write_goto(self, label: str) -> None:
        translated_command = self._command_translation_provider.get_command_translation(VMCmd.C_GOTO)\
            .format(str(self._current_function_scope), label)

        self.result += translated_command

    def _write_if(self, label: str):
        translated_command = self._command_translation_provider.get_command_translation(VMCmd.C_IF)\
            .format(str(self._current_function_scope), label)

        self.result += translated_command

    def _write_call(self, function_name: str, n_args: str) -> None:
        label_num: int = self._get_label_counter()
        translated_command = self._command_translation_provider.get_command_translation(VMCmd.C_CALL)\
            .format(function_name, label_num, n_args, function_name, function_name, label_num)

        self.result += translated_command

    def _write_return(self) -> None:
        translated_command = self._command_translation_provider.get_command_translation(VMCmd.C_RETURN)
        self.result += translated_command

    def _write_function(self, function_name: str, n_locals: str) -> None:
        translated_command = self._command_translation_provider.get_command_translation(VMCmd.C_FUNCTION)\
            .format(function_name, n_locals, function_name, function_name, function_name, function_name)
        self._current_function_scope = function_name

        self.result += translated_command
