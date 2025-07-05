import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Code, Image as ImageIcon, Play, Wand2 } from "lucide-react";

interface ToolPanelProps {
  activeTools: string[];
  codeContent: string;
  setCodeContent: (content: string) => void;
  codeLanguage: string;
  setCodeLanguage: (language: string) => void;
  imagePrompt: string;
  setImagePrompt: (prompt: string) => void;
  onGenerateImage: () => void;
  isGeneratingImage: boolean;
}

export default function ToolPanel({
  activeTools,
  codeContent,
  setCodeContent,
  codeLanguage,
  setCodeLanguage,
  imagePrompt,
  setImagePrompt,
  onGenerateImage,
  isGeneratingImage
}: ToolPanelProps) {
  return (
    <>
      {/* Code Editor Panel */}
      {activeTools.includes("code") && (
        <Card className="bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700">
          <CardContent className="p-4">
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center space-x-2">
                <Code className="h-4 w-4 text-orange-500" />
                <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                  Code Editor
                </span>
              </div>
              <div className="flex items-center space-x-2">
                <Select value={codeLanguage} onValueChange={setCodeLanguage}>
                  <SelectTrigger className="w-32">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="javascript">JavaScript</SelectItem>
                    <SelectItem value="python">Python</SelectItem>
                    <SelectItem value="html">HTML</SelectItem>
                    <SelectItem value="css">CSS</SelectItem>
                    <SelectItem value="typescript">TypeScript</SelectItem>
                    <SelectItem value="java">Java</SelectItem>
                    <SelectItem value="cpp">C++</SelectItem>
                  </SelectContent>
                </Select>
                <Button size="sm" className="bg-teal-600 hover:bg-teal-700 text-white">
                  <Play className="h-3 w-3 mr-1" />
                  Run
                </Button>
              </div>
            </div>
            <Textarea
              value={codeContent}
              onChange={(e) => setCodeContent(e.target.value)}
              placeholder="// Enter your code here..."
              className="w-full h-32 bg-gray-900 dark:bg-gray-800 text-green-400 font-mono text-sm p-3 rounded border border-gray-600 resize-none"
            />
          </CardContent>
        </Card>
      )}
      
      {/* Image Generation Panel */}
      {activeTools.includes("image") && (
        <Card className="bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700">
          <CardContent className="p-4">
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center space-x-2">
                <ImageIcon className="h-4 w-4 text-purple-500" />
                <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                  Image Generation
                </span>
              </div>
              <div className="flex items-center space-x-2">
                <Select defaultValue="dall-e-3">
                  <SelectTrigger className="w-32">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="dall-e-3">DALL-E 3</SelectItem>
                    <SelectItem value="midjourney">Midjourney</SelectItem>
                    <SelectItem value="stable-diffusion">Stable Diffusion</SelectItem>
                  </SelectContent>
                </Select>
                <Button 
                  size="sm" 
                  onClick={onGenerateImage}
                  disabled={isGeneratingImage || !imagePrompt.trim()}
                  className="bg-purple-600 hover:bg-purple-700 text-white"
                >
                  <Wand2 className="h-3 w-3 mr-1" />
                  {isGeneratingImage ? 'Generating...' : 'Generate'}
                </Button>
              </div>
            </div>
            <Input
              value={imagePrompt}
              onChange={(e) => setImagePrompt(e.target.value)}
              placeholder="Describe the image you want to generate..."
              className="w-full bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded px-3 py-2 text-sm"
            />
          </CardContent>
        </Card>
      )}
    </>
  );
}
