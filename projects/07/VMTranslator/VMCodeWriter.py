import os
from VMCommandTranslationProvider import VMCommandTranslationProvider
from VMConstant import VMCmd, VMSegment,\
    ARITHMETIC_COMMANDS, SEGMENT_TRANSLATION, TEMP_LOCATION_IN_RAM, IMPLEMENTATION_DIRECTORY


class VMCodeWriter:

    def __init__(self, asm_file_name, is_bootstrap_needed):
        self.asm_file_name = asm_file_name
        self.vm_file_name = None
        self.vm_file_name_without_dir = None

        self.command_translation_provider = VMCommandTranslationProvider(IMPLEMENTATION_DIRECTORY)
        self.result = ''
        self.current_function_scope = None

        self.label_counter = 0

        if is_bootstrap_needed:
            self.writeInit(self.getLabelCounter())

    def setFileName(self, vm_file_name):
        self.vm_file_name = vm_file_name
        self.vm_file_name_without_dir = os.path.basename(vm_file_name).rsplit('.', maxsplit=1)[0].strip()

    def getLabelCounter(self):
        result = self.label_counter
        self.label_counter += 1
        return result

    def writeCommand(self, command_name, arg1, arg2):
        if command_name in ARITHMETIC_COMMANDS:
            self.writeArithmetic(command_name, self.getLabelCounter())
        if command_name in [VMCmd.C_PUSH, VMCmd.C_POP]:
            self.writePushPop(command_name, arg1, arg2)
        if command_name == VMCmd.C_LABEL:
            self.writeLabel(arg1)
        if command_name == VMCmd.C_GOTO:
            self.writeGoto(arg1)
        if command_name == VMCmd.C_IF:
            self.writeIf(arg1)
        if command_name == VMCmd.C_FUNCTION:
            self.writeFunction(arg1, arg2)
        if command_name == VMCmd.C_CALL:
            self.writeCall(arg1, arg2, self.getLabelCounter())
        if command_name == VMCmd.C_RETURN:
            self.writeReturn()

    def writeArithmetic(self, command_name, label_num):

        translated_command = self.command_translation_provider.get_command_translation(command_name)
        if command_name in [VMCmd.C_EQ, VMCmd.C_GT, VMCmd.C_LT]:
            translated_command = translated_command.format(label_num, label_num, label_num, label_num)

        self.result += translated_command

    def writePushPop(self, command_name, segment, i):
        translated_command = self.command_translation_provider.get_command_translation(command_name, segment)

        if segment == VMSegment.S_CONSTANT:
            translated_command = translated_command.format(i)
        if segment in [VMSegment.S_LOCAL, VMSegment.S_ARGUMENT, VMSegment.S_THIS, VMSegment.S_THAT]:
            translated_command = translated_command.format(i, SEGMENT_TRANSLATION.get(segment))
        if segment == VMSegment.S_STATIC:
            translated_command = translated_command.format(self.vm_file_name_without_dir, i)
        if segment == VMSegment.S_TEMP:
            translated_command = translated_command.format(TEMP_LOCATION_IN_RAM, i)
        if segment == VMSegment.S_POINTER:
            new_segment = VMSegment.S_THIS if int(i) == 0 else VMSegment.S_THAT
            translated_command = translated_command.format(SEGMENT_TRANSLATION.get(new_segment))

        self.result += translated_command

    def writeInit(self, label_num):
        translated_command = self.command_translation_provider.get_command_translation(VMCmd.C_INIT)
        translated_command += self.command_translation_provider.get_command_translation(VMCmd.C_CALL) \
            .format('Sys.init', label_num, 0, 'Sys.init', 'Sys.init', label_num)

        self.result += translated_command

    def writeLabel(self, label):
        translated_command = self.command_translation_provider.get_command_translation(VMCmd.C_LABEL)\
            .format(str(self.current_function_scope), label)

        self.result += translated_command

    def writeGoto(self, label):
        translated_command = self.command_translation_provider.get_command_translation(VMCmd.C_GOTO)\
            .format(str(self.current_function_scope), label)

        self.result += translated_command

    def writeIf(self, label):
        translated_command = self.command_translation_provider.get_command_translation(VMCmd.C_IF)\
            .format(str(self.current_function_scope), label)

        self.result += translated_command

    def writeCall(self, function_name, n_args, label_num):
        translated_command = self.command_translation_provider.get_command_translation(VMCmd.C_CALL)\
            .format(function_name, label_num, n_args, function_name, function_name, label_num)

        self.result += translated_command

    def writeReturn(self):
        translated_command = self.command_translation_provider.get_command_translation(VMCmd.C_RETURN)
        self.result += translated_command

    def writeFunction(self, function_name, n_locals):
        translated_command = self.command_translation_provider.get_command_translation(VMCmd.C_FUNCTION)\
            .format(function_name, n_locals, function_name, function_name, function_name, function_name)
        self.current_function_scope = function_name

        self.result += translated_command

    def writeAsmFile(self):
        asm_file = open(self.asm_file_name, 'w')
        asm_file.write(self.result)
        asm_file.close()
