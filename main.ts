import { execSync } from 'node:child_process';
import { existsSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
if (!existsSync(outputDir)) {
  mkdirSync(outputDir, { recursive: true });
}

console.log('Generating news-image-20261124 front page via Python generator...');
execSync('python3 generate_image.py', { stdio: 'inherit' });

const target = join(outputDir, 'entry.png');
console.log(`Successfully generated and verified entry at ${target}`);
